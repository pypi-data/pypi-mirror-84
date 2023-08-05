#pylint: disable=too-many-lines
#pylint: disable=too-many-public-methods
"""
Unittests for the flipprogrammer class
"""
import unittest
from array import array
from intelhex import IntelHex

from mock import patch
from mock import call
from mock import MagicMock

from ..flipprogrammer import FlipProgrammer

VID = 0x03EB
PID = 0x2FEA

def flip_status_is_ok(status):
    """
    Helper function to replace flipprotocol mocked function status_is_ok
    """
    return status == 'STATUS_OK'

class TestFlipProgrammer(unittest.TestCase):
    """
    Unit tests for the FlipProgrammer class
    """

    def setUp(self):
        self.mock_flipprotocol_patch = patch('pydebuggerupgrade.flipprogrammer.FlipProtocol')
        self.mock_flipprotocol = self.mock_flipprotocol_patch.start()
        self.flipprotocol_mock_configure(self.mock_flipprotocol)
        self.mock_flipprotocol_obj = self.mock_flipprotocol.return_value

        # Using non default usb timeout to make sure it is propagated properly
        self.usb_timeout = 1

    @staticmethod
    def flipprotocol_mock_configure(mock_flipprotocol):
        """
        To be able to check for various attributes in the FlipProtocol class
        we have to make sure that the attributes used does return a string instead of
        just returning another MagicMock. This function configures an FlipProtocol mock to
        acheive this
        """
        mock_flipprotocol.configure_mock(MEMORY_UNIT_FLASH='MEMORY_UNIT_FLASH')

    def test_chip_erase_ok(self):
        """
        Test chip erase when flipprotocol responds with status OK
        """
        self.mock_flipprotocol_obj.chip_erase.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertTrue(flipprogrammer.chip_erase(self.usb_timeout))

        self.mock_flipprotocol_obj.chip_erase.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_chip_erase_failed(self):
        """
        Test chip erase when flipprotocol responds with status busy
        """
        self.mock_flipprotocol_obj.chip_erase.return_value = 'STATUS_ERASE_ONGOING'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertFalse(flipprogrammer.chip_erase(self.usb_timeout))

        self.mock_flipprotocol_obj.chip_erase.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_blank_check_flash_0x0000_0xffff_ok(self):
        """
        Test successful blank check from address 0x0000 to address 0xFFFF, i.e. all locations in page 0
        """
        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertTrue(flipprogrammer.blank_check_flash(0x0000, 0xFFFF, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls(
            [call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.blank_check.assert_has_calls([
            call.blank_check(0x0000, 0xFFFF, usb_timeout_ms=self.usb_timeout)])

    def test_blank_check_flash_0x00000_0x1ffff_ok(self):
        """
        Test successful blank check from address 0x00000 to 0x1FFFF,
        i.e. all locations in page 0 and all locations in page 1
        """
        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertTrue(flipprogrammer.blank_check_flash(0x0000, 0x1FFFF, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.blank_check.assert_has_calls([
            call.blank_check(0x0000, 0xFFFF, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.blank_check.assert_has_calls([
            call.blank_check(0x0000, 0xFFFF, usb_timeout_ms=self.usb_timeout)])

    def test_blank_check_flash_0x0ffff_0x10000_ok(self):
        """
        Test successful blank check from address 0x0FFFF to address 0x10000,
        i.e last location in page 0 and first location in page 1
        """
        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertTrue(flipprogrammer.blank_check_flash(0x0FFFF, 0x10000, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.blank_check.assert_has_calls([
            call.blank_check(0xFFFF, 0xFFFF, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.blank_check.assert_has_calls([
            call.blank_check(0x0000, 0x0000, usb_timeout_ms=self.usb_timeout)])

    def test_blank_check_select_memory_unit_outofrange(self):
        """
        Test blank check when select_memory_unit responds with STATUS_OUTOFRANGE
        """

        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OUTOFRANGE'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertFalse(flipprogrammer.blank_check_flash(0x0000, 0xFFFF, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])

    def test_blank_check_flash_select_page_outofrange(self):
        """
        Test blank check when select_page responds with STATUS_OUTOFRANGE
        """

        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OUTOFRANGE'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertFalse(flipprogrammer.blank_check_flash(0x0000, 0xFFFF, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])

    def test_blank_check_flash_blank_check_flash_failed(self):
        """
        Test failing blank check
        """

        self.mock_flipprotocol_obj.blank_check.return_value = 'STATUS_BLANK_FAIL'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        self.assertFalse(flipprogrammer.blank_check_flash(0x0000, 0xFFFF, self.usb_timeout))

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])

    def test_get_device_info_ok(self):
        """
        Test successful get_device_info
        """
        device_info = {'device_ids': {'manufacturer': 0xAA, 'family': 0xBB, 'device': 0xCC, 'revision': 0x01},
                       'bootloader_version': {'major': 0x02, 'minor': 0x01},
                       'bootloader_ids': {'ID1': 0x11, 'ID2': 0x22}}

        self.mock_flipprotocol_obj.get_device_ids.return_value = 'STATUS_OK', device_info['device_ids']
        self.mock_flipprotocol_obj.get_bootloader_version.return_value = 'STATUS_OK', device_info['bootloader_version']
        self.mock_flipprotocol_obj.get_bootloader_ids.return_value = 'STATUS_OK', device_info['bootloader_ids']
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        status, device_info_read = flipprogrammer.get_device_info(self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(device_info, device_info_read)

        self.mock_flipprotocol_obj.get_device_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)
        self.mock_flipprotocol_obj.get_bootloader_version.assert_called_with(usb_timeout_ms=self.usb_timeout)
        self.mock_flipprotocol_obj.get_bootloader_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_get_device_info_get_device_ids_failed(self):
        """
        Test get_device_info when get_device_ids fails
        """

        self.mock_flipprotocol_obj.get_device_ids.return_value = 'STATUS_MEM_UNKNOWN', None
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        status, device_info_read = flipprogrammer.get_device_info(self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(device_info_read)

        self.mock_flipprotocol_obj.get_device_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_get_device_info_get_bootloader_ids_failed(self):
        """
        Test get_device_info when get_bootloader_ids fails
        """
        device_info = {'device_ids': {'manufacturer': 0xAA, 'family': 0xBB, 'device': 0xCC, 'revision': 0x01},
                       'bootloader_version': {'major': 0x02, 'minor': 0x01},
                       'bootloader_ids': {'ID1': 0x11, 'ID2': 0x22}}

        self.mock_flipprotocol_obj.get_device_ids.return_value = 'STATUS_OK', device_info['device_ids']
        self.mock_flipprotocol_obj.get_bootloader_ids.return_value = 'STATUS_MEM_PROTECTED', None
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        status, device_info_read = flipprogrammer.get_device_info(self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(device_info_read)

        self.mock_flipprotocol_obj.get_device_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)
        self.mock_flipprotocol_obj.get_bootloader_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_get_device_info_get_bootloader_version_failed(self):
        """
        Test get_device_info when get_bootloader_version fails
        """
        device_info = {'device_ids': {'manufacturer': 0xAA, 'family': 0xBB, 'device': 0xCC, 'revision': 0x01},
                       'bootloader_version': {'major': 0x02, 'minor': 0x01},
                       'bootloader_ids': {'ID1': 0x11, 'ID2': 0x22}}

        self.mock_flipprotocol_obj.get_device_ids.return_value = 'STATUS_OK', device_info['device_ids']
        self.mock_flipprotocol_obj.get_bootloader_version.return_value = 'STATUS_OUTOFRANGE', None
        self.mock_flipprotocol_obj.get_bootloader_ids.return_value = 'STATUS_OK', device_info['bootloader_ids']
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        flipprogrammer = FlipProgrammer(VID, PID)

        status, device_info_read = flipprogrammer.get_device_info(self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(device_info_read)

        self.mock_flipprotocol_obj.get_device_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)
        self.mock_flipprotocol_obj.get_bootloader_version.assert_called_with(usb_timeout_ms=self.usb_timeout)
        self.mock_flipprotocol_obj.get_bootloader_ids.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_program_hex_1k_start_0x10000_2k_write_buffer_ok(self):
        """
        Test successful programming hex with 1 kbytes of data starting at address 0x10000, write buffer is 2 kbytes
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x10000
        hexfile_name = '1k_address_0x10000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 2048

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0000, data, 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_2k_write_buffer_ok(self):
        """
        Test successful programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 2 kbytes
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 2048

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0000, data, 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_1k_write_buffer_ok(self):
        """
        Test successful programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 1 kbytes
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 1024

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0000, data, 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_512_write_buffer_ok(self):
        """
        Test successful programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 512 bytes
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 512

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0000, data[0:512], 64, usb_timeout_ms=self.usb_timeout),
            call.program_start(0x0200, data[512:1024], 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0xffc0_512_write_buffer_ok(self):
        """
        Test successful programming hex with 1 kbytes of data starting at address 0xFFC0,
        write buffer is 512 bytes. This tests a write that spans two partial pages
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0xFFC0
        hexfile_name = '1k_address_0xFFC0.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 512

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([
            call.select_page(0, usb_timeout_ms=self.usb_timeout),
            call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0xFFC0, data[0:64], 64, usb_timeout_ms=self.usb_timeout),
            call.program_start(0x00000, data[64:576], 64, usb_timeout_ms=self.usb_timeout),
            call.program_start(0x0200, data[576:1024], 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_2k_write_buffer_select_memory_unit_outofrange(self):
        """
        Test failing programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 2 kbytes,
        when select_memory_unit responds with STATUS_OUTOFRANGE
        """

        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OUTOFRANGE'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 2048

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_2k_write_buffer_select_page_outofrange(self):
        """
        Test failing programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 2 kbytes,
        when select_page responds with STATUS_OUTOFRANGE
        """

        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OUTOFRANGE'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 2048

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x0000_2k_write_buffer_mem_protected(self):
        """
        Test failing programming hex with 1 kbytes of data starting at address 0x0000, write buffer is 2 kbytes,
        when memory is protected
        """
        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_MEM_PROTECTED'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x0000
        hexfile_name = '1k_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 2048

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0000, data, 64, usb_timeout_ms=self.usb_timeout)])

    def test_program_hex_1k_start_0x4_512_write_buffer_ok(self):
        """
        Test successful programming of hex with 1 kbytes of data starting at address 0x4, 512 bytes write buffer
        """

        self.mock_flipprotocol_obj.program_start.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        size = 1024
        start_address = 0x4
        hexfile_name = '1k_address_0x4.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.write_buffer_size = 512

        status = flipprogrammer.program_flash_from_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.program_start.assert_has_calls([
            call.program_start(0x0004, data[0:508], 64, usb_timeout_ms=self.usb_timeout),
            call.program_start(0x0200, data[508:1020], 64, usb_timeout_ms=self.usb_timeout),
            call.program_start(0x0400, data[1020:1024], 64, usb_timeout_ms=self.usb_timeout)])


    def test_read_flash_0x0000_to_0x03ff_1k_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0x0000 to 0x03ff (i.e. page 0), 1 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(0x400):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.return_value = 'STATUS_OK', data

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x0000, 0x03FF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x03FF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0x10000_to0x103ff_1k_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0x10000 to 0x103ff (i.e. page 1), 1 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(0x400):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.return_value = 'STATUS_OK', data

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x10000, 0x103FF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x03FF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0xfdff_to_0x105ff_1k_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0xFDFF to 0x105FF (i.e. both page 0 and 1), 1 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(2048):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.side_effect = [('STATUS_OK', data[0:512]),
                                                              ('STATUS_OK', data[512:1024]),
                                                              ('STATUS_OK', data[1024:2048])]

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0xFDFF, 0x105FF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([
            call.select_page(0, usb_timeout_ms=self.usb_timeout),
            call.select_page(1, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0xFDFF, 0xFFFF, usb_timeout_ms=self.usb_timeout),
            call.read_memory(0x0000, 0x03FF, usb_timeout_ms=self.usb_timeout),
            call.read_memory(0x0400, 0x05FF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0x0000_to_0x07ff_1k_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0x0000 to 0x07FF, 1 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(2048):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.side_effect = [('STATUS_OK', data[0:1024]),
                                                              ('STATUS_OK', data[1024:2048])]

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x0000, 0x07FF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x03FF, usb_timeout_ms=self.usb_timeout),
            call.read_memory(0x0400, 0x07FF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0x0000_to_0x03ff_512b_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0x0000 to 0x03FF, 512 bytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(0x400):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.side_effect = [('STATUS_OK', data[0:512]), ('STATUS_OK', data[512:1024])]

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 512

        status, data_read = flipprogrammer.read_flash(0x0000, 0x03FF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x01FF, usb_timeout_ms=self.usb_timeout),
            call.read_memory(0x0200, 0x03FF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0x0000_to_0x0fff_2k_read_buffer_ok(self):
        """
        Test succesfully reading flash from address 0x0000 to 0x0fff, 2 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(0x1000):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.side_effect = [('STATUS_OK', data[0:2048]),
                                                              ('STATUS_OK', data[2048:4096])]

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 2048

        status, data_read = flipprogrammer.read_flash(0x0000, 0x0FFF, self.usb_timeout)

        self.assertTrue(status)
        self.assertEqual(data, data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x07FF, usb_timeout_ms=self.usb_timeout),
            call.read_memory(0x0800, 0x0FFF, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_select_memory_outofrange(self):
        """
        Test reading flash when select_memory returns STATUS_OUTOFRANGE
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OUTOFRANGE'

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x0000, 0x03FF, self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_select_page_outofrange(self):
        """
        Test reading flash when select_page returns STATUS_OUTOFRANGE
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OUTOFRANGE'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x0000, 0x03FF, self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])

    def test_read_flash_0x0000_to_0x03ff_1k_read_buffer_mem_protected(self):
        """
        Test reading flash when read_memory returns STATUS_MEM_PROTECTED
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.select_page.return_value = 'STATUS_OK'
        self.mock_flipprotocol_obj.select_memory_unit.return_value = 'STATUS_OK'

        data = array('B', [])

        for i in range(0x400):
            data.append((i % 256) & 0xFF)

        self.mock_flipprotocol_obj.read_memory.return_value = 'STATUS_MEM_PROTECTED', None

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        status, data_read = flipprogrammer.read_flash(0x0000, 0x03FF, self.usb_timeout)

        self.assertFalse(status)
        self.assertIsNone(data_read)

        self.mock_flipprotocol_obj.select_memory_unit.assert_has_calls([
            call.select_memory_unit('MEMORY_UNIT_FLASH', usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.select_page.assert_has_calls([call.select_page(0, usb_timeout_ms=self.usb_timeout)])
        self.mock_flipprotocol_obj.read_memory.assert_has_calls([
            call.read_memory(0x0000, 0x03FF, usb_timeout_ms=self.usb_timeout)])

    def test_verify_flash_against_hex_2k_start_0x10000_1k_read_buffer_ok(self):
        """
        Test successful verify flash against hex, 2 kbytes, starting at 0x10000, 1 kbytes read buffer
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        size = 2048
        start_address = 0x10000
        hexfile_name = '2k_address_0x10000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        m_read_flash = MagicMock()
        with patch('pydebuggerupgrade.flipprogrammer.FlipProgrammer.read_flash', m_read_flash):
            m_read_flash.return_value = True, data
            status = flipprogrammer.verify_flash_against_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertTrue(status)

        m_read_flash.assert_called_with(0x10000, 0x107FF, usb_timeout_ms=self.usb_timeout)

    def test_verify_flash_against_hex_64b_start_0x0000_1k_read_buffer_byte_error_at_0x0002(self):
        """
        Test failing verify flash against hex, 64 bytes, starting at 0x0000, 1 kbytes read buffer,
        when there is a byte error at address 0x0002
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        size = 64
        start_address = 0x0000
        hexfile_name = '64b_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        # Inject error in data
        data[2] = 0xFF

        m_read_flash = MagicMock()
        with patch('pydebuggerupgrade.flipprogrammer.FlipProgrammer.read_flash', m_read_flash):
            m_read_flash.return_value = True, data
            status = flipprogrammer.verify_flash_against_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        m_read_flash.assert_called_with(0x0000, 0x003F, usb_timeout_ms=self.usb_timeout)

    def test_verify_flash_against_hex_64b_start_0x0000_1k_read_buffer_read_to_much(self):
        """
        Test failing verify flash against hex, 64 bytes, starting at 0x0000, 1 kbytes read buffer,
        when read_flash returns too much data
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        size = 64
        start_address = 0x0000
        hexfile_name = '64b_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        # Add one byte to the data to generate size mismatch
        data.append(0xFF)

        m_read_flash = MagicMock()
        with patch('pydebuggerupgrade.flipprogrammer.FlipProgrammer.read_flash', m_read_flash):
            m_read_flash.return_value = True, data
            status = flipprogrammer.verify_flash_against_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        m_read_flash.assert_called_with(0x0000, 0x003F, usb_timeout_ms=self.usb_timeout)

    def test_verify_flash_against_hex_64b_start_0x0000_1k_read_buffer_read_to_little(self):
        """
        Test failing verify flash against hex, 64 bytes, starting at 0x0000, 1 kbytes read buffer,
        when read_flash returns too little data
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        size = 64
        start_address = 0x0000
        hexfile_name = '64b_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        # Remove one byte from the data to generate size mismatch
        del data[63]

        m_read_flash = MagicMock()
        with patch('pydebuggerupgrade.flipprogrammer.FlipProgrammer.read_flash', m_read_flash):
            m_read_flash.return_value = True, data
            status = flipprogrammer.verify_flash_against_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        m_read_flash.assert_called_with(0x0000, 0x003F, usb_timeout_ms=self.usb_timeout)

    def test_verify_flash_against_hex_64b_start_0x0000_1k_read_buffer_read_failed(self):
        """
        Test failing verify flash against hex, 64 bytes, starting at 0x0000, 1 kbytes read buffer,
        when read_flash returns failure
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok

        size = 64
        start_address = 0x0000
        hexfile_name = '64b_address_0x0000.hex'
        data = array('B', [])

        for i in range(size):
            data.append(((i * 2) % 256) & 0xFF)

        # Make hex file containing some data
        hexfile = IntelHex()

        index = 0
        for byte in data:
            hexfile[index+start_address] = byte
            index += 1

        hexfile.write_hex_file(hexfile_name)

        flipprogrammer = FlipProgrammer(VID, PID)
        flipprogrammer.read_buffer_size = 1024

        m_read_flash = MagicMock()
        with patch('pydebuggerupgrade.flipprogrammer.FlipProgrammer.read_flash', m_read_flash):
            m_read_flash.return_value = False, None
            status = flipprogrammer.verify_flash_against_hex(hexfile_name, start_address, self.usb_timeout)

        self.assertFalse(status)

        m_read_flash.assert_called_with(0x0000, 0x003F, usb_timeout_ms=self.usb_timeout)

    def test_start_application_ok(self):
        """
        Test successful start_application
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.start_application.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        status = flipprogrammer.start_application(self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.start_application.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_crc_write_ok(self):
        """
        Test successful crc_write
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.crc_write.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        status = flipprogrammer.crc_write(self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.crc_write.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_clear_status_ok(self):
        """
        Test successful clear_status
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.clear_status.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        status = flipprogrammer.clear_status(self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.clear_status.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_abort_ok(self):
        """
        Test successful abort command
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.abort.return_value = 'STATUS_OK'

        flipprogrammer = FlipProgrammer(VID, PID)

        status = flipprogrammer.abort(self.usb_timeout)

        self.assertTrue(status)

        self.mock_flipprotocol_obj.abort.assert_called_with(usb_timeout_ms=self.usb_timeout)

    def test_clear_status_failed_mem_protected(self):
        """
        Test clear_status when STATUS_MEM_PROTECTED is returned
        """
        self.mock_flipprotocol_obj.status_is_ok = flip_status_is_ok
        self.mock_flipprotocol_obj.clear_status.return_value = 'STATUS_MEM_PROTECTED'

        flipprogrammer = FlipProgrammer(VID, PID)

        status = flipprogrammer.clear_status(self.usb_timeout)

        self.assertFalse(status)

        self.mock_flipprotocol_obj.clear_status.assert_called_with(usb_timeout_ms=self.usb_timeout)


if __name__ == '__main__':
    unittest.main()
