"""
Backend interface for the pydebuggerupgrade utility.

This module is the boundary between the Command Line Interface (CLI) part and
the backend part that does the actual job.  Any external utility or script that
needs access to the functionality provided by pydebuggerupgrade should connect to the
interface provided by this backend module.
"""
# Python 3 compatibility for Python 2
from __future__ import print_function

import time
import tempfile
import contextlib
import shutil

from logging import getLogger
from collections import namedtuple
from packaging import version

from .artifactprovider import get_available_artifact_versions, get_firmware_artifact_provider
from .artifactprovider import ArtifactRequest
from .artifactprovider import HexArtifactProvider
from .supported_tools import SUPPORTED_TOOLS
from .upgrader import Upgrader
from .pydebuggerupgrade_errors import PydebuggerupgradeNotSupportedError
from .pydebuggerupgrade_errors import PydebuggerupgradeError

# Static delay used to give a tool some time to reboot after an upgrade
# so that it is not detected as still in boot mode
BOOT_MODE_REBOOT_TIME = 0.5

# Note using mkdtemp instead of TemporaryDirectory for PY 2.7 compatibility
# Since mkdtemp does not automatically clean up (delete) the temporary directory
# it must be done manually by making a context manager
@contextlib.contextmanager
def tempdir(prefix):
    """A context manager for creating and then deleting a temporary directory."""
    tmpdir = tempfile.mkdtemp(prefix=prefix)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)

class Backend(object):
    """
    Backend interface of the pydebuggerupgrade utility.
    This class provides access to all the functionality provided by pydebuggerupgrade
    """

    API_VERSION = '2.2'

    def __init__(self, connect_timeout_s=10):
        """
        :param connect_timeout_s: timeout in seconds when attempting to connect to the tool
        """
        # Hook onto logger
        self.logger = getLogger(__name__)
        self.connect_timeout_s = connect_timeout_s

    def get_api_version(self):
        """
        Returns the current pydebuggerupgrade API version
        """
        return self.API_VERSION

    @staticmethod
    def get_available_versions(tool_name, repo=None, microchip_internal=False):
        """
        Returns a list of all available artifact versions based on the given parameters

        If microchip_internal is False this method will return a list of all
        tool pack versions on the pack server for the tool given by the tool_name.
        If the microchip_internal flag is True this method will return a list with:
          - all artifact versions in the Artifactory continuous repo if repo is 'continuous'
          - all artifact versions in the Artifactory stable repo if  repo is 'stable'
          - all artifact versions in the Artifactory release repo if repo is 'release'
        :param tool_name: Name of tool (e.g. 'nedbg')
        :param repo: Name of Artifactory repo to look up artifact versions in if microchip_internal is True.
            If microchip_internal is False this parameter is ignored.
        :param microchip_internal: If True versions will be looked up on the Microchip internal Artifactory server.
            If False versions will be looked up on the Microchip pack server (available externally)
        :return: List of versions of the matching artifacts available.
        """
        artifact_list = get_available_artifact_versions(tool_name, repo, microchip_internal)
        return artifact_list

    @staticmethod
    def resolve_and_fetch_firmware(artifact_request, temporary_dir):
        """
        Resolve the firmware artifact and fetch the hexfile

        Resolves the requested firmware artifact based on the provided parameters and fetches the firmware hex file
        from the artifact
        :param artifact_request: Instance of artifactprovider.ArtifactRequest with the parameters for the artifact
            to be resolved
        :param temporary_dir: Directory to be used as storage when fetching and unzipping the artifact
        :return namedtuple('firmware', ["hexfile", "version"])
            hexfile: Name and path of hexfile from the resolved artifact, None if no artifact or hexfile found
            version: Version of the fetched artifact, None if no artifact or hexfile found
        """
        logger = getLogger(__name__)
        Firmware = namedtuple('Firmware', ["hexfile", "version"])
        artifactprovider = get_firmware_artifact_provider(artifact_request, temporary_dir)
        if not artifactprovider.resolve():
            logger.error("Unable to find firmware artifact")
            return Firmware(None, None)

        target_version = artifactprovider.get_target_version()
        target_hexfile = artifactprovider.get_target_hexfile()

        return Firmware(hexfile=target_hexfile, version=target_version)

    @staticmethod
    def get_supported_tools():
        """
        Return a list with the names of all supported tools
        """
        tools_list = []
        for tool in SUPPORTED_TOOLS:
            tools_list.append(tool)

        return  tools_list

    @staticmethod
    def is_any_tool_in_bootmode(tool_name):
        """
        Check if any connected tools of the correct type already are in boot mode

        When a tool is in boot mode there is no USB serial number available.
        In other words it is not possible to separate two tools of the same type when both are in boot mode.
        :param tool_name: Name of tool (e.g. 'nedbg')
        :return: True if found matching tools already in boot mode

        :raises PydebuggerupgradeNotSupportedError if tool is not supported
        """
        Backend._check_if_tool_unsupported_and_raise(tool_name)
        upgrader = Upgrader()

        return upgrader.is_any_tool_in_bootmode(SUPPORTED_TOOLS[tool_name]['vid'], SUPPORTED_TOOLS[tool_name]['pid'])

    def upgrade_all_tools_in_bootmode(self, tool_name, hexfile):
        """
        Upgrade all matching tools already in boot mode

        :param tool_name: Name of tool (e.g. 'nedbg')
        :param hexfile: Name and path of hexfile to use for the upgrade
        """
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        vid = SUPPORTED_TOOLS[tool_name]['vid']
        pid = SUPPORTED_TOOLS[tool_name]['pid']

        upgrader = Upgrader()
        while upgrader.is_any_tool_in_bootmode(vid, pid):
            self.logger.info("Upgrading tool already in boot mode")
            upgrader.upgrade(vid, pid, hexfile, self.connect_timeout_s)

            # Give the tool some time to reboot after the upgrade
            # so that it is not detected as still in boot mode
            time.sleep(BOOT_MODE_REBOOT_TIME)

    @staticmethod
    def get_matching_tools(tool_name, serialnumber_substring=''):
        """
        Return a list of all matching tools connected to the host

        Note: pyedbglib uses 'serial_number' which is remapped here to 'serialnumber' for use in pydebuggerupgrade

        :param tool_name: Name of tool (e.g. 'nedbg')
        :param serialnumber_substring: Can be an empty string or a subset of a USB serial number.  Not case sensitive.
            This function will do matching of the last part of the device's USB serial numbers to
            the serialnumber_substring. Examples:
            '123' will match "MCHP3252000000043123" but not "MCP32520001230000000"
            '' will match any USB serial number
        :return: List with namedtuple('ToolInstance', 'name serialnumber') for all connected tools matching the
            tool_name and serialnumber_substring.  Note tools already in boot mode won't be listed.
        """
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        upgrader = Upgrader()
        tools_found = upgrader.get_matching_tools(SUPPORTED_TOOLS[tool_name]['usb_product_string'],
                                                  serialnumber_substring)

        ToolInstance = namedtuple('ToolInstance', 'name serialnumber')
        matching_tools = []
        for tool in tools_found:
            toolinstance = ToolInstance(tool_name, tool.serial_number)
            matching_tools.append(toolinstance)

        upgrader.take_down_transport()

        return matching_tools

    def get_current_version(self, tool_name, serialnumber):
        """
        Get current firmware version of a tool

        :param tool_name: Name of tool (e.g. 'nedbg')
        :param serialnumber: USB serial number of tool to access
        :return: version of tool firmware currently loaded

        :raises: PydebuggerupgradeError if
            - no matching tools found
            - more than one matching tool found
            - connection failed
        """
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        product_string = SUPPORTED_TOOLS[tool_name]['usb_product_string']
        upgrader = Upgrader()

        self.logger.info("Connecting to {0:s} '{1:s}'".format(product_string, serialnumber))

        upgrader.tool_connect(product_string, serialnumber)

        current_version = upgrader.get_current_version()

        upgrader.tool_disconnect()

        return current_version

    def resolve_source_version(self, source, tool_name='nedbg', microchip_internal=False):
        """
        Resolves firmware version of an upgrade candidate.
        :param source: source to use to upgrade
        :param tool_name: name of tool to upgrade
        :param microchip_internal: use Microchip internal artifact repository
        """
        # Check that this tool is supported
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        # Create an artifact request from the zipfile
        artifact_request = ArtifactRequest(tool_name, source, microchip_internal)

        # Unpack the ZIP in a temp location
        with tempdir(prefix='pydebuggerupgrade-') as temporary_dir:
            artifact = get_firmware_artifact_provider(artifact_request, temporary_dir)
            if not artifact.resolve():
                # Log error and continue (reporting)
                self.logger.error("Unable to resolve artifact source.")
                return ""

            if isinstance(artifact, HexArtifactProvider):
                # Hex files contain no readable version
                self.logger.error("Hex artifacts do not contain version information.")
                return "unknown"

            self.logger.info("Source contains firmware version: %s", artifact.version)
            return artifact.version

    def upgrade_from_source(self, source, tool_name='nedbg', serialnumber='', force=False, microchip_internal=False,
                            boot_mode=False):
        """
        Upgrades firmware from a given (bundled) zipfile.
        :param source: source to use to upgrade
        :param tool_name: name of tool to upgrade
        :param serialnumber: USB serial number of tool to upgrade
        :param force: force upgrade/downgrade even if up to date or older
        :param microchip_internal: use Microchip internal artifact repository
        :param boot_mode: scan for and upgrade all tools in boot mode
        """
        # Check that this tool is supported
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        # Create an artifact request from the zipfile
        artifact_request = ArtifactRequest(tool_name, source, microchip_internal)

        # Unpack the ZIP in a temp location
        with tempdir(prefix='pydebuggerupgrade-') as temporary_dir:
            artifact = get_firmware_artifact_provider(artifact_request, temporary_dir)
            if not artifact.resolve():
                raise PydebuggerupgradeError("Unable to resolve artifact source.")

            # In case of hexfile upgrade, use the force to avoid version checking
            if isinstance(artifact, HexArtifactProvider):
                force = True
                artifact.version = "unknown"

            self.logger.info("Source contains firmware version: %s", artifact.version)

            # Upgrade boot mode tools and return
            if boot_mode:
                self.upgrade_all_tools_in_bootmode(tool_name, artifact.get_target_hexfile())
                return True, artifact.version

            # Check the version currently installed on the tool
            current_version = self.get_current_version(tool_name, serialnumber)
            self.logger.info("Currently installed firmware: %s", current_version)

            # Version check and return if already OK.
            if not force and version.parse(current_version) >= version.parse(artifact.version):
                self.logger.info("Already up to date - skipping upgrade")
                return False, current_version

            # Upgrade
            self.upgrade_tool_from_hexfile(tool_name, serialnumber, artifact.get_target_hexfile())
            return True, artifact.version


    def upgrade_tool_from_hexfile(self, tool_name, serialnumber, hexfile):
        """
        Upgrade one tool from a hexfile source

        :param tool_name: Name of tool (e.g. 'nedbg')
        :param serialnumber: USB serial number of tool to upgrade
        :param hexfile: Name and path of hexfile to use for the upgrade

        :raises: PydebuggerupgradeError if
            - no matching tools found
            - more than one matching tool found
            - connection failed
        """
        Backend._check_if_tool_unsupported_and_raise(tool_name)

        product_string = SUPPORTED_TOOLS[tool_name]['usb_product_string']
        vid = SUPPORTED_TOOLS[tool_name]['vid']
        pid = SUPPORTED_TOOLS[tool_name]['pid']
        upgrader = Upgrader()

        self.logger.info("Connecting to {0:s} '{1:s}'".format(product_string, serialnumber))

        upgrader.tool_connect(product_string, serialnumber)
        # Note no need to call tool_disconnect as the enter_upgrade_mode will reboot tool and
        # thereby automatically disconnect
        upgrader.enter_upgrade_mode()
        upgrader.upgrade(vid, pid, hexfile, self.connect_timeout_s)

    @staticmethod
    def _check_if_tool_unsupported_and_raise(tool_name):
        if tool_name not in SUPPORTED_TOOLS:
            supported_tools = Backend.get_supported_tools()
            supported_tools_string = ', '.join([str(tool) for tool in supported_tools])
            error_msg = "{} is not supported.  Supported tools are: {}".format(tool_name, supported_tools_string)
            raise PydebuggerupgradeNotSupportedError(error_msg)
