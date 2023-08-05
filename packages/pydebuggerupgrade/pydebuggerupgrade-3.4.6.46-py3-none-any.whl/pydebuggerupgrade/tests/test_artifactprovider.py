# The intention is to make the test names descriptive enough to not need any docstrings for most of them
#pylint: disable=missing-docstring
"""
pydebuggerupgrade.artifactprovider module tests
"""
import unittest

from parameterized import parameterized
from mock import patch
from mock import MagicMock

from ..artifactprovider import get_available_artifact_versions

# Just some dummy versions to be used for testing purposes
DUMMY_VERSIONS_ARTIFACTORY = {'atmel': {'continuous': ['1.16.528', '1.15.527_some_branch'],
                                        'stable': ['1.6.300', '1.5.299'],
                                        'release':  ['1.20.600', '1.21.601', '1.21.602']
                                       },
                              'microchip': {'continuous': ['1.18.528', '1.18.527'],
                                            'stable': ['1.10.301'],
                                            'release':  ['1.10.500', '1.11.501']
                                           }
                             }

DUMMY_VERSIONS_PACKSERVER = ['1.1.11', '2.2.22', '3.3.33']

# To keep it simple all tests use the same parameters
TOOL = 'nedbg'
PACK_NAME = 'nEDBG_TP'

class TestArtifactProvider(unittest.TestCase):
    """
    artifactprovider module unit tests
    """
    def setUp(self):
        pass

    def _mock_requests_configure(self, return_no_artifacts=False):
        """
        Mock out Artifactory interaction.

        Mocks out requests module and sets up stub that returns dummy data for Artifactory requests
        """
        mock_get_patch = patch('pydebuggerupgrade.artifactprovider.get')
        self.addCleanup(mock_get_patch.stop)
        mock_get = mock_get_patch.start()

        if return_no_artifacts:
            mock_get.side_effect = self._requests_get_stub_no_artifacts
        else:
            mock_get.side_effect = self._requests_get_stub


    def _mock_packserver(self, return_no_artifacts=False):
        """
        Mock out PackServer class
        """
        mock_packserver_patch = patch('pydebuggerupgrade.artifactprovider.PackServer')
        self.addCleanup(mock_packserver_patch.stop)
        mock_packserver = mock_packserver_patch.start()

        # Create a mock that can be returned when the artifact provider creates a PackServer instance
        mock_packserver_obj = MagicMock()
        mock_packserver.return_value = mock_packserver_obj
        if return_no_artifacts:
            mock_packserver_obj.list_all_packs.return_value = {}
        else:
            # Just return a dictionary with at least one pack item.  This is not a correct response for list_all_packs,
            # but it is sufficient to fool the artifactprovider to think it has received a proper list of packs.
            # The fetch_pack_releases_for method will return the actual dummy versions
            mock_packserver_obj.list_all_packs.return_value = {PACK_NAME: '1.0'}

        pack_dict_list = []
        for version in DUMMY_VERSIONS_PACKSERVER:
            pack_dict_list.append({'version': version})
        mock_packserver_obj.fetch_pack_releases_for.return_value = pack_dict_list

    @staticmethod
    def _create_json_string(versions_list):
        json_string = '{"results": ['
        first = True
        for version in versions_list:
            if not first:
                json_string += ", "
            json_string += '{{"version": "{}"}}'.format(version)
            first = False
        json_string += "]}"
        return json_string

    def _requests_get_stub(self, url):
        """
        Stub to be used for mocking out requests.get calls

        Returns dummy data
        """
        mock_request_response = MagicMock()
        mock_request_response.status_code = 200
        if 'g=atmel' in url.lower():
            org = 'atmel'
        elif 'g=microchip' in url.lower():
            org = 'microchip'
        else:
            self.fail(msg="Uknown org in request URL: {}".format(url))

        if 'repos=ivy-stable' in url.lower():
            repo = 'stable'
        elif 'repos=ivy-release' in url.lower():
            repo = 'release'
        elif 'repos=ivy' in url.lower():
            repo = 'continuous'
        else:
            self.fail(msg="Uknown repo in request URL: {}".format(url))

        mock_request_response.text = self._create_json_string(DUMMY_VERSIONS_ARTIFACTORY[org][repo])
        return mock_request_response

    #pylint: disable=unused-argument
    def _requests_get_stub_no_artifacts(self, url):
        """
        Stub to be used for mocking out requests.get calls

        Returns empty list
        """
        mock_request_response = MagicMock()
        mock_request_response.status_code = 200
        mock_request_response.text = self._create_json_string([])
        return mock_request_response

    @parameterized.expand([
        ("continuous"),
        ("stable"),
        ("release"),
    ])
    def test_get_available_artifact_versions_microchip_internal(self, repo):
        dummy_versions_list = DUMMY_VERSIONS_ARTIFACTORY['atmel'][repo] + DUMMY_VERSIONS_ARTIFACTORY['microchip'][repo]

        self._mock_requests_configure(return_no_artifacts=False)

        artifact_list = get_available_artifact_versions(TOOL, repo, microchip_internal=True)

        self.assertEqual(set(artifact_list),
                         set(dummy_versions_list),
                         msg="get_available_artifact_versions did not return the expected list")

    def test_get_available_artifact_versions_packs(self):
        self._mock_packserver(return_no_artifacts=False)

        artifact_list = get_available_artifact_versions(TOOL, microchip_internal=False)

        self.assertEqual(artifact_list,
                         DUMMY_VERSIONS_PACKSERVER,
                         msg="get_available_artifact_versions did not return the expected list")

    def test_get_available_artifact_versions_artifactory_none_found_returns_empty_list(self):
        self._mock_requests_configure(return_no_artifacts=True)

        artifact_list = get_available_artifact_versions(TOOL, 'continuous', microchip_internal=True)

        self.assertEqual(artifact_list, [], msg="get_available_artifact_versions did not return the expected list")

    def test_get_available_artifact_versions_packserver_none_found_returns_empty_list(self):
        self._mock_packserver(return_no_artifacts=True)

        artifact_list = get_available_artifact_versions(TOOL, microchip_internal=False)

        self.assertEqual(artifact_list, [], msg="get_available_artifact_versions did not return the expected list")

    def test_get_available_artifact_versions_microchip_unkown_repo_returns_empty_list(self):
        self._mock_requests_configure(return_no_artifacts=False)

        artifact_list = get_available_artifact_versions(TOOL, 'unknown', microchip_internal=True)

        self.assertEqual(artifact_list, [], msg="get_available_artifact_versions did not return the expected list")
