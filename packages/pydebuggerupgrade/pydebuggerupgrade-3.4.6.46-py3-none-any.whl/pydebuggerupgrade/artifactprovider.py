"""
Provider of artifacts from various sources.  Used to find debugger firmware upgrade candidates.
"""
import os
import tempfile
import zipfile
import zlib
import xml.etree.ElementTree
import json

from logging import getLogger
from requests import get

from packaging.version import parse as versionparse

# These fields are only for use within the Microchip corporate network.
MICROCHIP_ARTIFACTORY_SERVER_URL = "https://artifacts.microchip.com/artifactory"
ARTIFACTORY_VERSIONS = ['release', 'stable', 'continuous']
TFP_VERSIONS = ['latest']

# These artifacts are supported
ARTIFACT_NAMES = {
    # Debugger PKOB nano (nEDBG)
    'nedbg': {
        # Firmware packs for this tool are called:
        'pack_name': "nEDBG_TP",
        # artifacts are distributed as:
        'ARTIFACT_NAMES': ["nedbg_fw.zip", "nedbg.zip"],
        # Within the zip arefacts, the hexfile is called:
        'hexfile_names': ["nedbg.hex"]
    },
    # Debugger PICkit4 (only for AVR image using special purpose DFU bootloader )
    'pickit4': {
        # Firmware packs for this tool are not available (since it is AVR image only and not stock bootloader)
        # Artifacts are distributed as:
        'ARTIFACT_NAMES': ["pickit4_fw_gcc.zip", "pickit4_fw_gcc_continuous.zip"],
        # Within the zip artifacts, these hexfiles are valid.
        'hexfile_names': ["pickit4.hex", "pickit4_fw.hex", "pickit4_fw_gcc.hex", "pickit4_fw_gcc_continuous.hex"],
    },
    # Debugger PICkit4 (only for AVR image using special purpose DFU bootloader )
    'snap': {
        # Firmware packs for this tool are not available (since it is AVR image only and not stock bootloader)
        # Artifacts are distributed as:
        'ARTIFACT_NAMES': ["snap_fw_gcc.zip", "snap_fw_gcc_continuous.zip"],
        # Within the zip artifacts, these hexfiles are valid.
        'hexfile_names': ["snap.hex", "snap_fw.hex", "snap_fw_gcc.hex", "snap_fw_gcc_continuous.hex"],
    }
}

# Primary artifact server settings
ARTIFACT_SOURCE_NEDBG_MICROCHIP = {
    'serves_tool': 'nedbg',
    'search_order': 1,
    'url': MICROCHIP_ARTIFACTORY_SERVER_URL,
    'org': "microchip",
    'module': "nedbg_fw"
}

# Alternative artifact server settings
ARTIFACT_SOURCE_NEDBG_ATMEL = {
    'serves_tool': 'nedbg',
    'search_order': 2,
    'url': MICROCHIP_ARTIFACTORY_SERVER_URL,
    'org': "atmel",
    'module': "nedbg",
}

# PICkit 4 artifact server settings (AVR image only)
ARTIFACT_SOURCE_PICKIT4_MICROCHIP = {
    'serves_tool': 'pickit4',
    'search_order': 1,
    'url': MICROCHIP_ARTIFACTORY_SERVER_URL,
    'org': "microchip",
    'module': "pickit4_fw_gcc"
}
# Snap artifact server settings (AVR image only)
ARTIFACT_SOURCE_SNAP_MICROCHIP = {
    'serves_tool': 'snap',
    'search_order': 1,
    'url': MICROCHIP_ARTIFACTORY_SERVER_URL,
    'org': "microchip",
    'module': "snap_fw_gcc"
}

# Full list of artifact servers
ARTIFACT_SERVERS = [
    ARTIFACT_SOURCE_NEDBG_ATMEL,
    ARTIFACT_SOURCE_NEDBG_MICROCHIP,
    ARTIFACT_SOURCE_PICKIT4_MICROCHIP,
    ARTIFACT_SOURCE_SNAP_MICROCHIP
    ]

# Constants used by various servers and artifacts
MANIFEST = "avrtools_fw.xml"
REPO_CONTINUOUS = "ivy"
REPO_STABLE = "ivy-stable"
REPO_RELEASE = "ivy-release"
REMOTE = "&remote=1"

# This class is a collection of parameters so no need for any methods
#pylint: disable=too-few-public-methods
class ArtifactRequest(object):
    """
    Collection of all parameters needed when requesting an artifact from external repositories

    Currently supported external repositories are the Microchip pack server (available outside Microchip network) and
    Artifactory (only available within Microchip network)
    Used as input parameter for the resolve_and_fetch_firmware method
    """

    def __init__(self, tool_name, artifact_id, microchip_internal=False):
        """
        :param tool_name: Name of the tool (e.g. 'nedbg') to fetch firmware artifact for
        :param artifact_id: Identifier for the artifact to fetch, either an exact version or a tag
            (e.g. 'latest', 'release' etc.)
        :param microchip_internal: Bool flag specifying if Microchip internal servers should be accessed
            (i.e. Microchip Artifactory)
        """
        self.artifact_id = artifact_id
        self.tool_name = tool_name
        self.microchip_internal = microchip_internal


def get_firmware_artifact_provider(artifact_request, temporary_dir):
    """
    Returns a suitable provider of artifacts given the inputs

    :param artifact_request: Instance of ArtifactRequest with request parameters
    :param temporary_dir: Directory to be used as temporary storage when fetching and unpacking artifacts
    :return: Artifact provider object according to the artifact_request parameters
    """
    getLogger(__name__).info("artifact provider for '%s' of '%s'",
                             artifact_request.artifact_id, artifact_request.tool_name)
    artifact_name = artifact_request.artifact_id
    if artifact_name.lower().endswith('hex'):
        # This is a HEX file already
        return HexArtifactProvider(artifact_request)
    if artifact_name.lower().endswith('.zip'):
        # This is a ZIP (hopefully containing hex and manifest)
        return ZipArtifactProvider(artifact_request, temporary_dir)
    if artifact_request.microchip_internal:
        # Internal artifacts
        if artifact_name in ARTIFACTORY_VERSIONS:
            # This is a request for an artifact of given status from Artifactory, eg: "stable"
            return StatusArtifactRepositoryArtifactProvider(artifact_request, temporary_dir)
        return VersionedArtifactRepositoryArtifactProvider(artifact_request, temporary_dir)

    # Public artifacts
    if artifact_name in TFP_VERSIONS:
        # This is a request for "latest" Tool Pack
        return LatestToolPackArtifactProvider(artifact_request, temporary_dir)
    # This is a specific Tool Pack version request
    return VersionedToolPackArtifactProvider(artifact_request, temporary_dir)

def get_available_artifact_versions(tool_name, repo=None, microchip_internal=False):
    """
    Returns a list of versions for all available artifacts for the given tool

    If microchip_internal is False the repo parameter is ignored and all artifact versions on the Microchip pack
    server (available externally) will be returned. If microchip_internal is True artifact versions will be looked up
    on the Microchip internal Artifactory server according to the repo parameter
    :param tool_name: Name of tool (e.g. 'nedbg')
    :param repo: Name of Artifactory repo to look up artifact versions in if microchip_internal is True.
        If microchip_internal is False this parameter is ignored.
    :param microchip_internal: If True artifact versions will be looked up on the Microchip internal Artifactory server.
        If False artifact versions will be looked up on the Microchip pack server (available externally)
    :return: List of versions representing the matching artifacts available.
    """
    if not microchip_internal:
        # For the artifact provider to find the correct provider for pack server access the repo must be set to 'latest'
        repo = 'latest'

    dummy_request = ArtifactRequest(tool_name, repo, microchip_internal)
    # No need for a temporary directory when just looking up artifacts (i.e. no fetching and unzipping)
    artifact_provider = get_firmware_artifact_provider(dummy_request, temporary_dir=None)
    if hasattr(artifact_provider, 'get_available_artifact_versions'):
        return artifact_provider.get_available_artifact_versions()
    return []

class ArtifactProvider(object):
    """
    Base class for provider of artifacts
    """

    def __init__(self, artifact_request, temporary_dir=None):
        self.logger = getLogger(__name__)
        self.artifact_request = artifact_request
        self.temporary_dir = temporary_dir
        self.logger.debug("init ArtifactProvider for '%s'", artifact_request.artifact_id)
        self.hexfile = None
        self.version = None

    # pylint: disable=no-self-use
    def resolve(self):
        """ Must be implemented by a derived class to be valid """
        return False

    def get_target_hexfile(self):
        """ Return resolved hexfile for upgrade """
        return self.hexfile

    def get_target_version(self):
        """ Return resolved version for upgrade """
        return self.version

    def _open_zip(self, zip_file_name):
        """
        Attempts to open a zip file and handles errors in doing so.

        :param zip_file_name: name of the file to open
        :return: zip file instance, None if no zip found
        """
        try:
            # Try to open ZIP file
            zipinstance = zipfile.ZipFile(zip_file_name)
        except IOError:
            # In Python 2.7 FileNotFoundError does not exist.  Instead an IOError will be raised.
            # In Python 3 IOError is the same as OSError and FileNotFoundError is a subclass of
            # OSError.  So catching IOError will work for both PY2.7 and PY3
            self.logger.error("File '%s' not found", zip_file_name)
            return None

        return zipinstance

    def _parse_manifest(self, xml_manifest, hexfile_names, namelist):
        """
        Parse the manifest looking for upgrade candidates

        :param xml_manifest: xml file documenting archive contents
        :param hexfile_names: list of acceptable hexfiles to look for
        :param namelist: list of actual contents of zip archive
        :return dictionary with filename and version, None if no upgrade candidates found
        """
        for child in xml_manifest:
            if child.attrib['filename'] in hexfile_names:
                upgrade_version = "{0:s}.{1:s}.{2:s}".format(child.attrib['major'], child.attrib['minor'],
                                                             child.attrib['build'])
                datestamp = xml_manifest.attrib['date']
                self.logger.info("Upgrade target artifact is version %s (dated %s)", upgrade_version, datestamp)
                # Look through the zip's own manifest
                for candidate in namelist():
                    # Look for all valid names for this tool
                    if candidate in hexfile_names:
                        self.logger.info("Found candidate '%s'", candidate)
                        return {'filename': candidate, 'version': upgrade_version}
        return None

    def extract_hexfile_from_zip(self, zip_file_name, hexfile_names):
        """
        Look in a zip archive and extract a hexfile which matches a name in the list

        The hexfile is stored for later use
        :param zip_file_name: zip file to open
        :param hexfile_names: names to match in the zip
        :return True if success
        """

        # Make sure the zip can be opened
        zip_file = self._open_zip(zip_file_name)
        if zip_file is None:
            return False

        # Try to extract content
        try:
            # Extract manifest file
            self.logger.info("Extracting manifest '%s' from zip", MANIFEST)
            manifest = zip_file.extract(MANIFEST, path=self.temporary_dir)
            xml_manifest = xml.etree.ElementTree.parse(manifest).getroot()
            # Parse the manifest
            candidate = self._parse_manifest(xml_manifest, hexfile_names, zip_file.namelist)
            if candidate is None:
                self.logger.error("Failed to find valid content in zip archive")
                zip_file.close()
                return False

            # Extract the candidate
            zip_file.extract(candidate['filename'], path=self.temporary_dir)
            zip_file.close()
        except KeyError:
            self.logger.error("Failed to extract hex file from zip")
            return False

        # Store results and report back
        self.hexfile = os.path.normpath(self.temporary_dir + "/" + candidate['filename'])
        self.version = candidate['version']
        return True


class ZipArtifactProvider(ArtifactProvider):
    """
    artifact provider for ZIP archives
    """

    def __init__(self, artifact_request, temporary_dir):
        ArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def resolve(self):
        """
        Zip files just need hex-extraction
        """
        zip_file = self.artifact_request.artifact_id
        return self.extract_hexfile_from_zip(zip_file,
                                             ARTIFACT_NAMES[self.artifact_request.tool_name]['hexfile_names'])


class HexArtifactProvider(ArtifactProvider):
    """
    artifact provider for HEX files
    """

    def __init__(self, artifact_request):
        ArtifactProvider.__init__(self, artifact_request)
        self.logger.info("HexArtifactProvider")

    def resolve(self):
        """
        Hex files need no work.
        But they have to exist
        """
        hex_file_name = os.path.normpath(self.artifact_request.artifact_id)
        if not os.path.exists(hex_file_name):
            self.logger.error("File not found: '%s'", hex_file_name)
            return False
        self.hexfile = hex_file_name
        # Return dummy version, since hexfiles are unversioned.  Implies that it needs a --force to work.
        self.version = "0.0.0"
        return True


class ArtifactRepositoryArtifactProvider(ArtifactProvider):
    """
    artifact provider for artifacts served by an artifactory repository, such as Archiva or Artifactory
    """

    def __init__(self, artifact_request, temporary_dir):
        ArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def _iterate_filelist_and_attempt_download(self, file_list, repo, server, version):
        """
        Iterates the file list and attempts to download the artifact version from the server
        """
        # Try each file in the list
        for target_file in file_list:
            # Construct the URL
            artifact_url = "/{0:s}/{1:s}/{2:s}/{3:s}/{4:s}".format(repo, server['org'], server['module'], version,
                                                                   target_file)
            self.logger.info("Trying: %s%s", server['url'], artifact_url)
            # Make the request
            artifact = get(server['url'] + artifact_url)
            self.logger.info("Fetch returned '%s:%s'", artifact.status_code, artifact.reason)
            if artifact.status_code == 200:
                # Success.  Now extract.
                zip_file = self._store_artifactory_artifact_to_zipfile(self.artifact_request.tool_name,
                                                                       artifact.content)
                return self.extract_hexfile_from_zip(zip_file,
                                                     ARTIFACT_NAMES[self.artifact_request.tool_name]['hexfile_names'])

        return False

    def _store_artifactory_artifact_to_zipfile(self, artifact_name, content):
        """
        Stores a zip artifact in a temp location and returns the path to it
        """
        temporary_file = tempfile.NamedTemporaryFile(prefix="{}_".format(artifact_name), suffix=".zip", delete=False,
                                                     dir=self.temporary_dir)
        self.logger.info("Writing to temporary file %s", temporary_file.name)
        temporary_file.write(content)
        temporary_file.close()
        return temporary_file.name

    def _get_server_list(self):
        # Find servers which can serve this usb device
        servers = []
        for server in ARTIFACT_SERVERS:
            if server['serves_tool'] == self.artifact_request.tool_name:
                servers.append(server)

        return servers


class StatusArtifactRepositoryArtifactProvider(ArtifactRepositoryArtifactProvider):
    """
    artifact provider for artifacts served by an artifactory repository.
    This provider operates on status requests like "continuous", "stable" or "release"
    """

    def __init__(self, artifact_request, temporary_dir):
        ArtifactRepositoryArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def resolve(self):
        """
        Fetches the artifact from Artifactory
        Saves the ZIP file into a temp file
        Unzips and saves a temp hexfile and returns
        """
        self.logger.info(self.temporary_dir)
        if self.artifact_request.artifact_id == "release":
            self.logger.info("Upgrading to latest released firmware")
            repo = REPO_RELEASE
        elif self.artifact_request.artifact_id == "stable":
            self.logger.info("Upgrading to latest stable firmware.")
            repo = REPO_STABLE
        else:
            self.logger.info("Upgrading to latest integration (continuous) firmware.")
            repo = REPO_CONTINUOUS

        # Find servers which can serve this usb device
        servers = self._get_server_list()

        # There can be several artifact servers, sort by search order
        for server in sorted(servers, key=lambda i: (i['search_order'])):
            search_url = "/api/search/latestVersion?g={0:s}&a={1:s}&repos={2:s}{3:s}".format(server['org'],
                                                                                             server['module'], repo,
                                                                                             REMOTE)
            self.logger.info("Fetching latest %s from %s repository on %s", self.artifact_request.artifact_id,
                             server['org'], server['url'])
            latest = get(server['url'] + search_url)
            if latest.status_code == 200:
                version = latest.text
                self.logger.info("Latest %s build is %s", self.artifact_request.artifact_id, version)
                file_list = []
                # Construct file list
                for artifact_name in ARTIFACT_NAMES[self.artifact_request.tool_name]['ARTIFACT_NAMES']:
                    file_name = "{0:s}-{1:s}{2:s}".format(os.path.splitext(artifact_name)[0], version,
                                                          os.path.splitext(artifact_name)[1])
                    file_list.append(file_name)

                if self._iterate_filelist_and_attempt_download(file_list, repo, server, version):
                    return True
        return False

    def get_available_artifact_versions(self):
        """
        Return a list of the versions of all artifacts available in the repo for the configured tool
        """
        if self.artifact_request.artifact_id == "release":
            repo = REPO_RELEASE
        elif self.artifact_request.artifact_id == "stable":
            repo = REPO_STABLE
        else:
            repo = REPO_CONTINUOUS
        versions_list = []
        for server in self._get_server_list():
            search_url = "/api/search/versions?g={0:s}&a={1:s}&repos={2:s}{3:s}".format(server['org'],
                                                                                        server['module'],
                                                                                        repo,
                                                                                        REMOTE)
            self.logger.info("Looking up all %s versions from %s repository on %s", self.artifact_request.artifact_id,
                             server['org'], server['url'])
            versions_response = get(server['url'] + search_url)
            if versions_response.status_code == 200:
                versions = json.loads(versions_response.text)
                for version_dict in versions['results']:
                    version = version_dict['version']
                    versions_list.append(version)

        return versions_list


class VersionedArtifactRepositoryArtifactProvider(ArtifactRepositoryArtifactProvider):
    """
    artifact provider for artifacts served by an artifactory repository.
    This provider operates on exact versions, like 1.2.3
    """

    def __init__(self, artifact_request, temporary_dir):
        ArtifactRepositoryArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def resolve(self):
        """
        Fetches the artifact from Artifactory
        Saves the ZIP file into a temp file
        Unzips and saves a temp hexfile and returns
        """
        # Version we are looking for:
        version = self.artifact_request.artifact_id

        # Look in:
        repos = [REPO_RELEASE, REPO_STABLE, REPO_CONTINUOUS]

        file_list = []
        for artifact_name in ARTIFACT_NAMES[self.artifact_request.tool_name]['ARTIFACT_NAMES']:
            file_name = "{0:s}-{1:s}{2:s}".format(os.path.splitext(artifact_name)[0], version,
                                                  os.path.splitext(artifact_name)[1])
            file_list.append(file_name)

        # Find servers which can serve this usb device
        servers = self._get_server_list()

        # There can be several artifact servers, sort by search order
        for server in sorted(servers, key=lambda i: (i['search_order'])):
            # And several repos on each server
            for repo in repos:
                if self._iterate_filelist_and_attempt_download(file_list, repo, server, version):
                    return True
        return False


class ToolPackArtifactProvider(ArtifactProvider):
    """
    artifact provider for artifacts served by a pack server
    """

    def __init__(self, artifact_request, temporary_dir):
        ArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def _connect_to_packserver(self, pack_name):
        # Connect to the pack server
        pack_server = PackServer()

        # Download the list of all packs - check that there exists one
        pack_list = pack_server.list_all_packs()
        if pack_name not in pack_list:
            self.logger.error("Pack repo contains no relevant packs for %s", self.artifact_request.tool_name)
            return None
        return pack_server

    def unpack_pack(self, packfile):
        """
        Unpacks the given pack
        """
        self.logger.debug("Unpacking %s", packfile)
        pack_zip = self._open_zip(packfile)
        if pack_zip is None:
            return False
        try:
            # Try to extract content
            self.logger.info("Extracting from zip")
            for candidate in pack_zip.namelist():
                if os.path.basename(candidate) in ARTIFACT_NAMES[self.artifact_request.tool_name]['ARTIFACT_NAMES']:
                    self.logger.info("Extracting %s", candidate)
                    fw_zip = pack_zip.extract(candidate, path=self.temporary_dir)
                    return self.extract_hexfile_from_zip(fw_zip, ARTIFACT_NAMES[self.artifact_request.tool_name][
                        'hexfile_names'])
        except KeyError:
            pack_zip.close()
            self.logger.error("Failed to extract hex file from zip")
            return False
        return False

    def get_available_artifact_versions(self):
        """
        Return a list of the versions of all artifacts available on the pack server for the configured tool
        """
        pack_name = ARTIFACT_NAMES[self.artifact_request.tool_name]['pack_name']
        pack_server = self._connect_to_packserver(pack_name)
        if pack_server is None:
            return []

        packlist = pack_server.fetch_pack_releases_for(pack_name)

        versions_list = []
        for pack in packlist:
            versions_list.append(pack['version'])

        return versions_list


class LatestToolPackArtifactProvider(ToolPackArtifactProvider):
    """
    artifact provider for artifacts served by a pack server
    This provider operates on a tag "latest" which gives only the latest released pack release
    """

    def __init__(self, artifact_request, temporary_dir):
        ToolPackArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def resolve(self):
        """
        Look for the latest pack released
        """
        version = self.artifact_request.artifact_id
        pack_name = ARTIFACT_NAMES[self.artifact_request.tool_name]['pack_name']
        if version != 'latest':
            raise Exception("Use 'latest' for unversioned TFP upgrade")

        # Connect to the pack server
        pack_server = self._connect_to_packserver(pack_name)
        if pack_server is None:
            return False

        # And look for all releases of that pack
        self.logger.info("Looking for releases for %s", pack_name)
        matching_packlist = pack_server.fetch_pack_releases_for(pack_name)
        self.logger.info("%d releases found", len(matching_packlist))
        if not matching_packlist:
            self.logger.error("No pack releases found!")
            return False
        # Find latest available
        latest = matching_packlist[0]['version']
        for release in matching_packlist:
            if versionparse(release['version']) > versionparse(latest):
                latest = release
        # Fetch it
        packfile = pack_server.fetch_pack(pack_name, latest, self.temporary_dir)
        self.logger.info("Pack fetched")
        return self.unpack_pack(packfile)


class VersionedToolPackArtifactProvider(ToolPackArtifactProvider):
    """
    artifact provider for artifacts served by a pack server
    This provider operates on an absolute pack release value like 1.2.3
    """

    def __init__(self, artifact_request, temporary_dir):
        ToolPackArtifactProvider.__init__(self, artifact_request, temporary_dir)

    def resolve(self):
        """
        Look for the specific pack
        """
        version = self.artifact_request.artifact_id
        pack_name = ARTIFACT_NAMES[self.artifact_request.tool_name]['pack_name']

        # Connect to the pack server
        pack_server = self._connect_to_packserver(pack_name)
        if pack_server is None:
            return False

        matching_packlist = pack_server.fetch_pack_releases_for(pack_name)
        for pack_version in matching_packlist:
            if versionparse(pack_version['version']) == versionparse(version):
                self.logger.info("Match found")
                packfile = pack_server.fetch_pack(pack_name, version, self.temporary_dir)
                self.logger.info("Pack fetched")
                return self.unpack_pack(packfile)
        return False


PACK_SERVER_MICROCHIP = 'https://packs.download.microchip.com'
PACK_SERVER_ATMEL = 'http://packs.download.atmel.com'
PACK_SERVER_DEFAULT = PACK_SERVER_MICROCHIP
PACK_INDEX_NAMESPACE = 'http://packs.download.atmel.com/pack-idx-atmel-extension'


class PackServer(object):
    """
    Connection to remote pack server
    """

    def __init__(self):
        self.logger = getLogger(__name__)
        self.pack_index = None

    def _fetch_pack_idx(self, server=PACK_SERVER_DEFAULT):
        """
        Fetch the pack index
        :param server: server URL to connect to
        """
        url = server + '/index.idx.gz'
        response = get(url)
        idx_xml = zlib.decompress(response.content, zlib.MAX_WBITS | 32)
        self.pack_index = xml.etree.ElementTree.fromstring(idx_xml)

    def _get_pack_idx(self):
        """
        Return pack index (cache)
        """
        if self.pack_index is None:
            self._fetch_pack_idx()
        return self.pack_index

    def _fetch_packs_for(self, packtype):
        """
        Return list of all packs for a given type

        :param packtype: type of pack to look for
        :return list of packs
        """
        idx = self._get_pack_idx()
        return idx.findall('./pdsc[@atmel:name="{}"]'.format(packtype), namespaces={'atmel': PACK_INDEX_NAMESPACE})

    @staticmethod
    def _fetch_releases_for(pack):
        """
        Return list of releases for the pack

        :param pack: pack instance from the pack index
        :return list of releases
        """
        return pack.findall('atmel:releases/atmel:release', namespaces={'atmel': PACK_INDEX_NAMESPACE})

    def list_all_packs(self):
        """
        Return list of all packs
        """
        idx = self._get_pack_idx()
        packs = []
        for pack in idx.findall('./pdsc'):
            packs.append(pack.attrib.get('{{{}}}name'.format(PACK_INDEX_NAMESPACE)))
        return packs

    def fetch_pack_releases_for(self, packtype):
        """
        Return list of all pack releases for a given type

        :params packtype: type of pack to look for
        :return: list of release dictionaries with version and description
        """
        releases = []

        for pack in self._fetch_packs_for(packtype):
            for release in self._fetch_releases_for(pack):
                self.logger.debug("Found pack version '%s'", release.attrib.get('version'))
                releases.append(
                    {'version': release.attrib.get('version'), 'description': release.getchildren()[0].text})

        return releases

    def fetch_pack(self, packtype, version, path):
        """
        Fetch a release version of a given pack and store it to a given path

        :param packtype: type of pack to fetch
        :param version: version to retrieve
        :param path: path to store pack
        :return: filename of the fetched pack
        """
        # Go right in and fetch this pack since its version is known
        self.logger.debug("Fetching pack '%s' for '%s'", version, packtype)
        url = "{0:s}/Microchip.{1:s}.{2:s}.atpack".format(PACK_SERVER_DEFAULT, packtype, version)
        req = get(url, allow_redirects=True, stream=True)
        filename = "{0:s}//{1:s}.{2:s}.zip".format(path, packtype, version)
        with open(filename, 'wb') as file_content:
            for chunk in req.iter_content(chunk_size=128):
                file_content.write(chunk)
        return filename
