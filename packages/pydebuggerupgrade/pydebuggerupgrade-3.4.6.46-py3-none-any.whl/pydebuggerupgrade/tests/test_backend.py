# The intention is to make the test names descriptive enough to not need any docstrings for most of them
#pylint: disable=missing-docstring
# It seems better to have all tests for one module in the same file than to split across multiple files,
# so accepting many public methods and many lines makes sense
#pylint: disable=too-many-lines
#pylint: disable=too-many-public-methods
"""
pydebuggerupgrade backend API tests

These tests validates the API used by external front-ends/scripts
"""
import unittest
import shutil
import os

from distutils.version import LooseVersion
from collections import namedtuple
from mock import patch
from mock import MagicMock
from mock import call

from ..backend import Backend
from ..artifactprovider import ArtifactRequest
from ..pydebuggerupgrade_errors import PydebuggerupgradeNotSupportedError

TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tempfiles')

# To keep it simple all tests use the same tool
TOOL = 'nedbg'
PID = 0x2FC0
VID = 0x03EB
PRODUCT_STRING = 'nedbg'
TOOL_UNSUPPORTED = 'notool'
CONNECT_TIMEOUT_S = 3

class TestBackend(unittest.TestCase):
    """
    pydebuggerupgrade backend API unit tests
    """
    def setUp(self):
        # Make sure no relics from previous tests mess up the current test
        try:
            shutil.rmtree(TEMP_FOLDER)
        except FileNotFoundError:
            # Folder is already gone
            pass
        # Then make the empty folder for use in the tests
        os.mkdir(TEMP_FOLDER)

        self.backend = Backend(CONNECT_TIMEOUT_S)

    def _mock_upgrader(self):
        """
        Mocking out Upgrader object
        """
        mock_upgrader_patch = patch('pydebuggerupgrade.backend.Upgrader')
        self.addCleanup(mock_upgrader_patch.stop)
        mock_upgrader = mock_upgrader_patch.start()
        # Fetch the mock that will be returned when the Backend creates an Upgrader instance
        mock_upgrader_obj = mock_upgrader.return_value

        return mock_upgrader_obj

    def test_get_api_version_returns_major_version_1_or_higher(self):
        api_version_read = self.backend.get_api_version()

        self.assertGreaterEqual(LooseVersion(api_version_read), LooseVersion('1.0'))

    @patch('pydebuggerupgrade.backend.get_available_artifact_versions')
    def test_get_available_artifact_versions_propagrates_all_parameters(self, mock_get_available_artifact_versions):
        artifact_id = 'release'
        tool = 'nedbg'
        dummy_artifact_list = ['dummy']

        mock_get_available_artifact_versions.return_value = dummy_artifact_list

        artifact_list = self.backend.get_available_versions(tool, artifact_id, microchip_internal=True)

        self.assertEqual(artifact_list, dummy_artifact_list, msg="get_artifact_list did not return the expected list")
        mock_get_available_artifact_versions.assert_called_with(tool, artifact_id, True)

    def test_resolve_and_fetch_firmware_pack_latest(self):
        request = ArtifactRequest('nedbg', 'latest', microchip_internal=False)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNotNone(firmware.hexfile)
        self.assertIsNotNone(firmware.version)

    def test_resolve_and_fetch_firmware_artifactory_continuous(self):
        request = ArtifactRequest('nedbg', 'continuous', microchip_internal=True)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNotNone(firmware.hexfile)
        self.assertIsNotNone(firmware.version)

    def test_resolve_and_fetch_firmware_artifactory_stable(self):
        request = ArtifactRequest('nedbg', 'stable', microchip_internal=True)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNotNone(firmware.hexfile)
        self.assertIsNotNone(firmware.version)

    def test_resolve_and_fetch_firmware_artifactory_release(self):
        request = ArtifactRequest('nedbg', 'release', microchip_internal=True)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNotNone(firmware.hexfile)
        self.assertIsNotNone(firmware.version)

    def test_resolve_and_fetch_firmware_versioned_pack_artifact_not_found_returns_none(self):
        request = ArtifactRequest('nedbg', '0.0.0', microchip_internal=False)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNone(firmware.hexfile)
        self.assertIsNone(firmware.version)

    def test_resolve_and_fetch_firmware_versioned_artifactory_artifact_not_found_returns_none(self):
        request = ArtifactRequest('nedbg', '0.0.0', microchip_internal=True)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNone(firmware.hexfile)
        self.assertIsNone(firmware.version)

    def test_resolve_and_fetch_firmware_artifactory_repo_not_found_returns_none(self):
        request = ArtifactRequest('nedbg', 'unknown', microchip_internal=True)
        firmware = self.backend.resolve_and_fetch_firmware(request, TEMP_FOLDER)

        self.assertIsNone(firmware.hexfile)
        self.assertIsNone(firmware.version)

    def test_get_supported_tools(self):
        expected_tools = ['nedbg', 'pickit4', 'snap']

        supported_tools = self.backend.get_supported_tools()

        self.assertEqual(set(expected_tools), set(supported_tools))

    def test_is_any_tool_in_bootmode_propagates_all_parameters(self):
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.is_any_tool_in_bootmode.return_value = True

        in_bootmode = self.backend.is_any_tool_in_bootmode(TOOL)

        self.assertTrue(in_bootmode)
        mock_upgrader.is_any_tool_in_bootmode.assert_called_with(VID, PID)

    def test_is_any_tool_in_bootmode_raises_pydebuggerupgradenotsupportederror_when_tool_unsupported(self):
        with self.assertRaises(PydebuggerupgradeNotSupportedError):
            self.backend.is_any_tool_in_bootmode(TOOL_UNSUPPORTED)

    def test_upgrade_all_tools_in_bootmode_when_none_in_bootmode(self):
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.is_any_tool_in_bootmode.return_value = False

        self.backend.upgrade_all_tools_in_bootmode(TOOL, None)

        mock_upgrader.upgrade.assert_not_called()

    def test_upgrade_all_tools_in_bootmode_when_one_in_bootmode(self):
        dummyhex = 'somehex.hex'
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.is_any_tool_in_bootmode.side_effect = [True, False]

        self.backend.upgrade_all_tools_in_bootmode(TOOL, dummyhex)

        mock_upgrader.upgrade.assert_called_once_with(VID, PID, dummyhex, CONNECT_TIMEOUT_S)

    def test_upgrade_all_tools_in_bootmode_when_two_in_bootmode(self):
        dummyhex = 'somehex.hex'
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.is_any_tool_in_bootmode.side_effect = [True, True, False]

        self.backend.upgrade_all_tools_in_bootmode(TOOL, dummyhex)

        mock_upgrader.has_calls(
            [
                call.upgrade(VID, PID, dummyhex),
                call.upgrade(VID, PID, dummyhex)
            ]
        )

        self.assertEqual(mock_upgrader.upgrade.call_count, 2, msg="Only two upgrades should be run")

    def test_upgrade_all_tools_in_bootmode_raises_pydebuggerupgradenotsupportederror_when_tool_unsupported(self):
        with self.assertRaises(PydebuggerupgradeNotSupportedError):
            self.backend.upgrade_all_tools_in_bootmode(TOOL_UNSUPPORTED, None)

    def test_get_matching_tools_propagates_all_parameters(self):
        serialnumber = '12345'

        mock_upgrader = self._mock_upgrader()
        mock_upgrader.get_matching_tools.return_value = []

        self.backend.get_matching_tools(TOOL, serialnumber)

        mock_upgrader.get_matching_tools.assert_called_with(PRODUCT_STRING, serialnumber)
        mock_upgrader.take_down_transport.assert_called()

    def test_get_matching_tools_raises_pydebuggerupgradenotsupportederror_when_tool_unsupported(self):
        with self.assertRaises(PydebuggerupgradeNotSupportedError):
            self.backend.get_matching_tools(TOOL_UNSUPPORTED)

    def test_get_matching_tools_none_found_returns_empty_list(self):
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.get_matching_tools.return_value = []

        tools_found = self.backend.get_matching_tools(TOOL)

        self.assertEqual(tools_found, [])

    def test_get_matching_tools_one_found(self):
        serialnumber = '12345'
        serialnumber_substring = '45'

        mock_tool = MagicMock()
        mock_tool.product_string = PRODUCT_STRING
        mock_tool.serial_number = serialnumber
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.get_matching_tools.return_value = [mock_tool]

        tools_found = self.backend.get_matching_tools(TOOL, serialnumber_substring)

        ToolInstance = namedtuple('ToolInstance', 'name serialnumber')
        expected_tool = ToolInstance(TOOL, serialnumber)
        self.assertEqual(tools_found, [expected_tool])

    def test_get_matching_tools_two_found(self):
        serialnumber_a = '12345'
        serialnumber_b = 'MCHP123456745'
        serialnumber_substring = '45'

        mock_tool_a = MagicMock()
        mock_tool_a.product_string = PRODUCT_STRING
        mock_tool_a.serial_number = serialnumber_a
        mock_tool_b = MagicMock()
        mock_tool_b.product_string = PRODUCT_STRING
        mock_tool_b.serial_number = serialnumber_b
        mock_upgrader = self._mock_upgrader()
        mock_upgrader.get_matching_tools.return_value = [mock_tool_a, mock_tool_b]

        tools_found = self.backend.get_matching_tools(TOOL, serialnumber_substring)

        ToolInstance = namedtuple('ToolInstance', 'name serialnumber')
        expected_tool_a = ToolInstance(TOOL, serialnumber_a)
        expected_tool_b = ToolInstance(TOOL, serialnumber_b)
        self.assertEqual(tools_found, [expected_tool_a, expected_tool_b])

    def test_get_current_version_connects_and_propagates_all_parameters(self):
        serialnumber = '12345'
        version = '1.1.1'

        mock_upgrader = self._mock_upgrader()
        mock_upgrader.get_current_version.return_value = version

        current_version = self.backend.get_current_version(TOOL, serialnumber)

        self.assertEqual(current_version, version)
        mock_upgrader.tool_connect.assert_called_with(PRODUCT_STRING, serialnumber)
        mock_upgrader.tool_disconnect.assert_called()
        mock_upgrader.get_current_version.assert_called()

    def test_get_current_version_raises_pydebuggerupgradenotsupportederror_when_tool_unsupported(self):
        with self.assertRaises(PydebuggerupgradeNotSupportedError):
            self.backend.get_current_version(TOOL_UNSUPPORTED, '')

    def test_upgrade_tool_from_hexfile(self):
        serialnumber = '12345'
        dummyhex = 'somehex.hex'

        mock_upgrader = self._mock_upgrader()

        self.backend.upgrade_tool_from_hexfile(TOOL, serialnumber, dummyhex)

        mock_upgrader.tool_connect.assert_called_with(TOOL, serialnumber)
        # Note no need for upgrader to call tool_disconnect as the enter_upgrade_mode will
        # reboot tool and thereby automatically disconnect
        mock_upgrader.enter_upgrade_mode.assert_called()
        mock_upgrader.upgrade.assert_called_with(VID, PID, dummyhex, CONNECT_TIMEOUT_S)

    def test_upgrade_tool_from_hexfile_raises_pydebuggerupgradenotsupportederror_when_tool_unsupported(self):
        with self.assertRaises(PydebuggerupgradeNotSupportedError):
            self.backend.upgrade_tool_from_hexfile(TOOL_UNSUPPORTED, '', 'somehex.hex')

    def test_upgrade_from_source(self):
        # TODO
        pass
