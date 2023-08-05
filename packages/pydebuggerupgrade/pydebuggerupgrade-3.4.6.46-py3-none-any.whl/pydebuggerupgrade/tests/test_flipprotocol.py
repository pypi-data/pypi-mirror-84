#pylint: disable=too-many-lines
#pylint: disable=too-many-public-methods
"""
Partial integration tests testing the FlipProtocol and DfuProtocol classes.
"""
import unittest
from array import array

from mock import patch
from mock import Mock
from mock import call
import usb.core

from ..flipprotocol import FlipProtocol

VID = 0x03EB
PID = 0x2FEA

TIMEOUT_MS = 5000

DFU_REQ_IN = 0xA1
DFU_REQ_OUT = 0x21

# Calls and responses to USB layer
CALL_GET_STATUS = call.ctrl_transfer(DFU_REQ_IN, 3, 0, 0, 6, TIMEOUT_MS)
CALL_CLR_STATUS = call.ctrl_transfer(DFU_REQ_OUT, 4, 0, 0, None, TIMEOUT_MS)
CALL_ABORT = call.ctrl_transfer(DFU_REQ_OUT, 6, 0, 0, None, TIMEOUT_MS)

RSP_STATUS_OK = array('B', [0x00, 0x00, 0x00, 0x00, 0x02, 0x00])
RSP_STATUS_STALL = array('B', [0x0F, 0x00, 0x00, 0x00, 0x0A, 0x00])
RSP_STATUS_OUTOFRANGE = array('B', [0x08, 0x00, 0x00, 0x00, 0x0A, 0x00])
RSP_STATUS_MEM_PROTECTED = array('B', [0x03, 0x00, 0x00, 0x00, 0x00, 0x00])
RSP_STATUS_MEM_UNKNOWN = array('B', [0x03, 0x00, 0x00, 0x00, 0x0A, 0x00])
RSP_STATUS_ERASE_ONGOING = array('B', [0x09, 0x00, 0x00, 0x00, 0x04, 0x00])
RSP_STATUS_BLANK_FAIL = array('B', [0x05, 0x00, 0x00, 0x00, 0x00, 0x00])

FLIP_CMD_CHIP_ERASE = [0x04, 0x00, 0xFF, 0x00, 0x00, 0x00]
FLIP_CMD_START_APPLICATION = [0x04, 0x03, 0x00, 0x00, 0x00, 0x00]
FLIP_CMD_CRC_WRITE = [0x04, 0x01, 0x00, 0x00, 0x00, 0x00]

def call_dfu_dnload(data):
    """
    Generates DFU DNLOAD request calls with given data

    Arguments:
    data -- list of bytes to download to device
    """
    return call.ctrl_transfer(DFU_REQ_OUT, 1, 0, 0, data, TIMEOUT_MS)

def call_dfu_upload(num_bytes):
    """
    Generates DFU UPLOAD request call with given number of bytes

    Arguments:
    num_bytes -- number of bytes to upload from device
    """
    return call.ctrl_transfer(DFU_REQ_IN, 2, 0, 0, num_bytes, TIMEOUT_MS)

def flip_cmd_read(start_address, end_address):
    """
    Generates the payload for the DFU DNLOAD command of a FLIP Read memory command

    Arguments:
    start_address -- 16-bit start address
    end_address -- 16-bit end address
    """
    # MSB first of addresses
    return [0x03,
            0x00,
            (start_address >> 8) & 0xff,
            start_address & 0xFF,
            (end_address >> 8) & 0xFF,
            end_address & 0xFF]

def flip_cmd_blank_check(start_address, end_address):
    """
    Generates the payload for the DFU DNLOAD command of a FLIP blank check command

    Arguments:
    start_address -- 16-bit start address
    end_address -- 16-bit end address
    """
    # MSB first of addresses
    return [0x03,
            0x01,
            (start_address >> 8) & 0xff,
            start_address & 0xFF,
            (end_address >> 8) & 0xFF,
            end_address & 0xFF]

def flip_cmd_select_page(page):
    """
    Generates the payload for the DFU DNLOAD command of a FLIP Select page command

    Arguments:
    page -- 16-bit page number (each FLIP page is 64KB)
    """
    # MSB first of page number
    return [0x06, 0x03, 0x01, (page >> 8) & 0xff, page & 0xFF, 0x00]

def flip_cmd_select_memory_unit(unit):
    """
    Generates the payload for the DFU DNLOAD command of a FLIP Select memory unit command

    Arguments:
    page -- 8-bit memory unit ID
    """
    return [0x06, 0x03, 0x00, unit & 0xff, 0x00, 0x00]

def flip_cmd_program_start(start_address, data, memory_write_entity=0):
    """
    Generates the payload for the DFU DNLOAD command of a FLIP program start command

    Arguments:
    start_address -- 16-bit start address
    data -- list of bytes to write to memory
    """
    # End is last location to be written
    end = start_address + len(data) - 1
    cmd = [0x01, 0x00, (start_address >> 8) & 0xff, start_address & 0xFF, (end >> 8) & 0xFF, end & 0xFF]

    # FLIP command should be 64 bytes
    cmd.extend([0x00] * 58)

    if memory_write_entity > 0:
        # Pad with 0xFF before data to align with memory_write_entity
        cmd.extend([0xFF] * (start_address%memory_write_entity))

    cmd.extend(data)

    return cmd

class TestFlipProtocol(unittest.TestCase):
    """
    Partial integration tests testing the FlipProtocol and DfuProtocol classes.
    """

    def setUp(self):
        self.mock_dfuusbdevice_patch = patch('pydebuggerupgrade.dfuprotocol.DfuUsbDevice')
        self.mock_dfuusbdevice = self.mock_dfuusbdevice_patch.start()
        self.mock_dfuusbdevice_obj = self.mock_dfuusbdevice.return_value

        # Mock out the USB layer
        self.mock_usb = Mock()
        self.mock_dfuusbdevice_obj.connect.return_value = self.mock_usb

    def test_sign_on_ok_first_attempt(self):
        """
        Test sign_on, successful on first attempt
        """
        self.mock_usb.ctrl_transfer.return_value = RSP_STATUS_OK

        flip = FlipProtocol(VID, PID, 1)

        self.assertTrue(flip.sign_on())
        self.mock_usb.ctrl_transfer.assert_has_calls([CALL_GET_STATUS])

    def test_sign_on_ok_first_stall_then_ok(self):
        """
        Test sign_on, first attempt receives STATUS_STALL, second attempt after clearing status is succesful
        """
        self.mock_usb.ctrl_transfer.side_effect = [RSP_STATUS_STALL, None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        self.assertTrue(flip.sign_on())

        self.mock_usb.assert_has_calls([CALL_GET_STATUS, CALL_CLR_STATUS, CALL_GET_STATUS])

    def test_sign_on_not_ok_first_stall_then_stall(self):
        """
        Test failing sign_on, first attempt and second attempt after clearing status receives STATUS_STALL
        """
        self.mock_usb.ctrl_transfer.side_effect = [RSP_STATUS_STALL, None, RSP_STATUS_STALL]

        flip = FlipProtocol(VID, PID, 1)

        self.assertFalse(flip.sign_on())

        self.mock_usb.assert_has_calls([CALL_GET_STATUS, CALL_CLR_STATUS, CALL_GET_STATUS])

    def test_read_memory_4bytes_ok(self):
        """
        Test successful memory read of 4 bytes
        """
        data_expected = array('B', [0x00, 0x01, 0x02, 0x03])
        self.mock_usb.ctrl_transfer.side_effect = [None, data_expected, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, data = flip.read_memory(0, 3)

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(data_expected, data)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_read(0, 3)), call_dfu_upload(4), CALL_GET_STATUS])

    def test_read_memory_64bytes_ok(self):
        """
        Test successful memory read of 64 bytes
        """
        data_expected = array('B', range(64))
        self.mock_usb.ctrl_transfer.side_effect = [None, data_expected, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, data = flip.read_memory(0, 63)

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(data_expected, data)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_read(0, 63)), call_dfu_upload(64), CALL_GET_STATUS])

    def test_read_memory_70bytes_ok(self):
        """
        Test successful memory read of 70 bytes
        """
        data_expected = array('B', range(70))
        self.mock_usb.ctrl_transfer.side_effect = [None, data_expected, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, data_rsp = flip.read_memory(0, 69)

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(data_expected, data_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_read(0, 69)), call_dfu_upload(70), CALL_GET_STATUS])

    def test_read_memory_status_outofrange(self):
        """
        Test failing memory read receiving STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status, data_rsp = flip.read_memory(0, 3)

        self.assertEqual('STATUS_OUTOFRANGE', status)
        self.assertIsNone(data_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_read(0, 3)), CALL_GET_STATUS])

    def test_read_memory_status_mem_protected(self):
        """
        Test failing memory read receiving STATUS_MEM_PROTECTED
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, usb.core.USBError("Error msg"), RSP_STATUS_MEM_PROTECTED]

        flip = FlipProtocol(VID, PID, 1)

        status, data_rsp = flip.read_memory(0, 3)

        self.assertEqual('STATUS_MEM_PROTECTED', status)
        self.assertIsNone(data_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_read(0, 3)), call_dfu_upload(4), CALL_GET_STATUS])


    def test_read_device_id_ok(self):
        """
        Test successful read of device ID
        """
        ids = array('B', [0x11, 0x22, 0x33, 0x44])

        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None, ids, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, id_rsp = flip.get_device_ids()

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(ids[0], id_rsp['manufacturer'])
        self.assertEqual(ids[1], id_rsp['family'])
        self.assertEqual(ids[2], id_rsp['device'])
        self.assertEqual(ids[3], id_rsp['revision'])

        self.mock_usb.assert_has_calls([
            call_dfu_dnload(flip_cmd_select_memory_unit(0x05)),
            CALL_GET_STATUS,
            call_dfu_dnload(flip_cmd_read(0, 3)),
            call_dfu_upload(4),
            CALL_GET_STATUS])

    def test_read_device_id_select_memory_unit_outofrange(self):
        """
        Test failing read of device ID, select_memory_unit receiving STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status, id_rsp = flip.get_device_ids()

        self.assertEqual('STATUS_OUTOFRANGE', status)
        self.assertIsNone(id_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x05)), CALL_GET_STATUS])

    def test_read_device_id_read_outofrange(self):
        """
        Test failing read of device ID, final status read as STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status, id_rsp = flip.get_device_ids()

        self.assertEqual('STATUS_OUTOFRANGE', status)
        self.assertIsNone(id_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x05)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(0, 3)),
                                        CALL_GET_STATUS])

    def test_read_device_id_read_mem_protected(self):
        """
        Test failing read of device ID, final status read as STATUS_MEM_PROTECTED
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   None,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_MEM_PROTECTED]

        flip = FlipProtocol(VID, PID, 1)

        status, id_rsp = flip.get_device_ids()

        self.assertEqual('STATUS_MEM_PROTECTED', status)
        self.assertIsNone(id_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x05)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(0, 3)),
                                        call_dfu_upload(4),
                                        CALL_GET_STATUS])

    def test_chip_erase_no_retries_ok_first_attempt(self):
        """
        Test chip_erase without retries, successful on first attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(0)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE), CALL_GET_STATUS])

    def test_chip_erase_no_retries_not_finished(self):
        """
        Test chip_erase without retries, failing with STATUS_ERASE_ONGOING
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_ERASE_ONGOING]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(0)

        self.assertEqual('STATUS_ERASE_ONGOING', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE), CALL_GET_STATUS])

    def test_chip_erase_one_retry_ok_second_attempt(self):
        """
        Test chip_erase with one retry, successful on second attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_ERASE_ONGOING, None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(1)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS])

    def test_chip_erase_one_retry_ok_first_attempt(self):
        """
        Test chip_erase with one retry, successful on first attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(1)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE), CALL_GET_STATUS])

    def test_chip_erase_one_retry_not_finished(self):
        """
        Test chip_erase with one retry, failing with STATUS_ERASE_ONGOING on both attempts
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_ERASE_ONGOING, None, RSP_STATUS_ERASE_ONGOING]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(1)

        self.assertEqual('STATUS_ERASE_ONGOING', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS])

    def test_chip_erase_two_retries_ok_third_attempt(self):
        """
        Test chip_erase with two retries (i.e. total of three attempts), success after third attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_ERASE_ONGOING,
                                                   None,
                                                   RSP_STATUS_ERASE_ONGOING,
                                                   None,
                                                   RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(2)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS])

    def test_chip_erase_two_retries_ok_second_attempt(self):
        """
        Test chip_erase with two retries (i.e. total of three attempts), success after second attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_ERASE_ONGOING, None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(2)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS])

    def test_chip_erase_two_retries_not_finished(self):
        """
        Test chip_erase with two retries (i.e. total of three attempts),
        failing with STATUS_ERASE_ONGOING after each attempt
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_ERASE_ONGOING,
                                                   None,
                                                   RSP_STATUS_ERASE_ONGOING,
                                                   None,
                                                   RSP_STATUS_ERASE_ONGOING]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.chip_erase(2)

        self.assertEqual('STATUS_ERASE_ONGOING', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(FLIP_CMD_CHIP_ERASE),
                                        CALL_GET_STATUS])

    def test_blank_check_from_0_to_0_ok(self):
        """
        Test successful blank check of one location
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.blank_check(0, 0)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_blank_check(0, 0)), CALL_GET_STATUS])

    def test_blank_check_from_0x10_to_0x110_ok(self):
        """
        Test successful blank check from address 0x10 to 0x110
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.blank_check(0x10, 0x110)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_blank_check(0x10, 0x110)), CALL_GET_STATUS])

    def test_blank_check_from_0_to_0_mem_unknown(self):
        """
        Test blank check of one location, failing with STATUS_MEM_UNKNOWN
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_MEM_UNKNOWN]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.blank_check(0x10, 0x110)

        self.assertEqual('STATUS_MEM_UNKNOWN', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_blank_check(0x10, 0x110)), CALL_GET_STATUS])

    def test_blank_check_from_0_to_0_blank_fail(self):
        """
        Test blank check of one location, failing with STATUS_BLANK_FAIL
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_BLANK_FAIL]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.blank_check(0x10, 0x110)

        self.assertEqual('STATUS_BLANK_FAIL', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_blank_check(0x10, 0x110)), CALL_GET_STATUS])

    def test_select_page_0_ok(self):
        """
        Test successful select_page 0 (first page)
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_page(0)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_page(0)), CALL_GET_STATUS])

    def test_select_page_0x102_ok(self):
        """
        Test successful select_page 0x102 (one random page in the middle)
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_page(0x102)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_page(0x102)), CALL_GET_STATUS])

    def test_select_page_0xffff_ok(self):
        """
        Test successful select_page 0xFFFF (last page)
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_page(0xFFFF)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_page(0xFFFF)), CALL_GET_STATUS])

    def test_select_page_0_outofrange(self):
        """
        Test select_page 0 failing with STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_page(0)

        self.assertEqual('STATUS_OUTOFRANGE', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_page(0)), CALL_GET_STATUS])

    def test_select_memory_unit_0x07_ok(self):
        """
        Test successful select_memory_unit 0x07
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_memory_unit(0x07)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x07)), CALL_GET_STATUS])

    def test_select_memory_unit_0x20_outofrange(self):
        """
        Test select_memory_unit 0x20 failing with STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.select_memory_unit(0x20)

        self.assertEqual('STATUS_OUTOFRANGE', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x20)), CALL_GET_STATUS])

    def test_program_start_0x0000_0x0000_pagesize_0_ok(self):
        """
        Test program_start (download data to device memory), one location, pagesize (memory_write_entity) of 0,
        i.e. no padding
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', [0xAA])

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(0x0000, data_expected)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(0x0000, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x00ff_0x0100_pagesize_0_ok(self):
        """
        Test program_start (download data to device memory) from address 0x00FF to 0x0100,
        pagesize (memory_write_entity) of 0, i.e. no padding
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', [0xAA, 0xBB])
        start = 0x00FF

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(start, data_expected)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(start, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x0102_0x0103_pagesize_0_ok(self):
        """
        Test program_start (download data to device memory) from address 0x0102 to 0x0103 (two locations),
        pagesize (memory_write_entity) of 0, i.e. no padding
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', [0xAA, 0xBB])
        start = 0x0102

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(start, data_expected)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(start, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x0000_0x003f_pagesize_0_ok(self):
        """
        Test program_start (download data to device memory) from address 0x0000 to 0x03F,
        pagesize (memory_write_entity) of 0, i.e. no padding
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', range(64))
        start = 0x0000

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(start, data_expected)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(start, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x0000_0x0100_pagesize_0_ok(self):
        """
        Test program_start (download data to device memory) from address 0x0000 to 0x0100,
        pagesize (memory_write_entity) of 0, i.e. no padding
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', range(256))
        data_expected.append(0x00)
        start = 0x0000

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(start, data_expected)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(start, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x00ff_0x0100_pagesize_64_ok(self):
        """
        Test program_start (download data to device memory) from address 0x00FF to 0x0100,
        pagesize (memory_write_entity) of 64, i.e. pad to align with page start boundary
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        data_expected = array('B', [0xAA, 0xBB])
        start = 0x00FF

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(start, data_expected, 64)

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(start, data_expected, 64)),
                                        CALL_GET_STATUS])


    def test_program_start_0x0000_0x0000_pagesize_0_mem_protected(self):
        """
        Test program_start (download data to device memory) one location, failing with STATUS_MEM_PROTECTED
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_MEM_PROTECTED]

        data_expected = array('B', [0xAA])

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(0x0000, data_expected)

        self.assertEqual('STATUS_MEM_PROTECTED', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(0x0000, data_expected)),
                                        CALL_GET_STATUS])

    def test_program_start_0x0000_0x0000_pagesize_0_mem_unknown(self):
        """
        Test program_start (download data to device memory) one location, failing with STATUS_MEM_UNKNOWN
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_MEM_UNKNOWN]

        data_expected = array('B', [0xAA])

        flip = FlipProtocol(VID, PID, 1)

        status = flip.program_start(0x0000, data_expected)

        self.assertEqual('STATUS_MEM_UNKNOWN', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_program_start(0x0000, data_expected)),
                                        CALL_GET_STATUS])

    def test_get_bootloader_version_ok(self):
        """
        Test successful get_bootloader_version
        """
        versions = array('B', [0xAB])
        major = 0x0A
        minor = 0x0B

        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None, versions, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, version_rsp = flip.get_bootloader_version()

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(major, version_rsp['major'])
        self.assertEqual(minor, version_rsp['minor'])

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(0, 0)),
                                        call_dfu_upload(1),
                                        CALL_GET_STATUS])

    def test_get_bootloader_version_select_memory_unit_outofrange(self):
        """
        Test get_bootloader_version failing with STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status, version_rsp = flip.get_bootloader_version()

        self.assertEqual('STATUS_OUTOFRANGE', status)
        self.assertIsNone(version_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)), CALL_GET_STATUS])

    def test_get_bootloader_version_read_mem_unknown(self):
        """
        Test get_bootloader_version failing with STATUS_MEM_UNKNOWN
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_MEM_UNKNOWN]

        flip = FlipProtocol(VID, PID, 1)

        status, version_rsp = flip.get_bootloader_version()

        self.assertEqual('STATUS_MEM_UNKNOWN', status)
        self.assertIsNone(version_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(0, 0)),
                                        CALL_GET_STATUS])

    def test_get_bootloader_version_mem_protected(self):
        """
        Test get_bootloader_version failing with STATUS_MEM_PROTECTED
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   None,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_MEM_PROTECTED]

        flip = FlipProtocol(VID, PID, 1)

        status, version_rsp = flip.get_bootloader_version()

        self.assertEqual('STATUS_MEM_PROTECTED', status)
        self.assertIsNone(version_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(0, 0)),
                                        call_dfu_upload(1),
                                        CALL_GET_STATUS])

    def test_get_bootloader_ids_ok(self):
        """
        Test successful get_bootloader_ids
        """
        ids = array('B', [0xAA, 0xBB])

        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None, ids, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status, ids_rsp = flip.get_bootloader_ids()

        self.assertEqual('STATUS_OK', status)
        self.assertEqual(ids[0], ids_rsp['ID1'])
        self.assertEqual(ids[1], ids_rsp['ID2'])

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(1, 2)),
                                        call_dfu_upload(2),
                                        CALL_GET_STATUS])

    def test_get_bootloader_ids_select_memory_unit_outofrange(self):
        """
        Test get_bootloader_ids, select_memory_unit failing with STATUS_OUTOFRANGE
        """
        self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_OUTOFRANGE]

        flip = FlipProtocol(VID, PID, 1)

        status, ids_rsp = flip.get_bootloader_ids()

        self.assertEqual('STATUS_OUTOFRANGE', status)
        self.assertIsNone(ids_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)), CALL_GET_STATUS])

    def test_get_bootloader_ids_read_mem_unknown(self):
        """
        Test failing get_bootloader_ids, final get_status returning STATUS_MEM_UNKOWN
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_MEM_UNKNOWN]

        flip = FlipProtocol(VID, PID, 1)

        status, ids_rsp = flip.get_bootloader_ids()

        self.assertEqual('STATUS_MEM_UNKNOWN', status)
        self.assertIsNone(ids_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(1, 2)),
                                        CALL_GET_STATUS])

    def test_get_bootloader_ids_mem_protected(self):
        """
        Test failing get_bootloader_ids, final get_status returning STATUS_MEM_PROTECTED
        """
        self.mock_usb.ctrl_transfer.side_effect = [None,
                                                   RSP_STATUS_OK,
                                                   None,
                                                   usb.core.USBError("Error msg"),
                                                   RSP_STATUS_MEM_PROTECTED]

        flip = FlipProtocol(VID, PID, 1)

        status, ids_rsp = flip.get_bootloader_ids()

        self.assertEqual('STATUS_MEM_PROTECTED', status)
        self.assertIsNone(ids_rsp)

        self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x04)),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload(flip_cmd_read(1, 2)),
                                        call_dfu_upload(2),
                                        CALL_GET_STATUS])

    def test_start_application_ok(self):
        """
        Test successful start_application
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.start_application()

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_START_APPLICATION),
                                        CALL_GET_STATUS,
                                        call_dfu_dnload([])])

    def test_crc_write_ok(self):
        """
        Test successful crc_write
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.crc_write()

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([call_dfu_dnload(FLIP_CMD_CRC_WRITE), CALL_GET_STATUS])


    def test_clear_status_ok(self):
        """
        Test successful clear_status
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.clear_status()

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([CALL_CLR_STATUS, CALL_GET_STATUS])

    def test_clear_status_mem_unknown(self):
        """
        Test clear_status failing with STATUS_MEM_UNKOWN
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_MEM_UNKNOWN]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.clear_status()

        self.assertEqual('STATUS_MEM_UNKNOWN', status)

        self.mock_usb.assert_has_calls([CALL_CLR_STATUS, CALL_GET_STATUS])

    def test_abort_ok(self):
        """
        Test successful abort command
        """
        self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK]

        flip = FlipProtocol(VID, PID, 1)

        status = flip.abort()

        self.assertEqual('STATUS_OK', status)

        self.mock_usb.assert_has_calls([CALL_ABORT, CALL_GET_STATUS])

    # Some tests of features not implemented yet, might be implemented in future DFU bootloaders
    # def test_is_secured_true_ok(self):
    #     self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None, [0x01], RSP_STATUS_OK]

    #     flip = FlipProtocol(VID, PID, 1)

    #     status, secured_rsp = flip.is_secured()

    #     self.assertEqual('STATUS_OK', status)
    #     self.assertEqual(True, secured_rsp)

    #     self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x02)),
    #                                     CALL_GET_STATUS,
    #                                     call_dfu_dnload(flip_cmd_read(0, 0)),
    #                                     call_dfu_upload(1),
    #                                     CALL_GET_STATUS])

    # def test_is_secured_false_ok(self):
    #     self.mock_usb.ctrl_transfer.side_effect = [None, RSP_STATUS_OK, None, [0x00], RSP_STATUS_OK]

    #     flip = FlipProtocol(VID, PID, 1)

    #     status, secured_rsp = flip.is_secured()

    #     self.assertEqual('STATUS_OK', status)
    #     self.assertEqual(False, secured_rsp)

    #     self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x02)),
    #                                     CALL_GET_STATUS,
    #                                     call_dfu_dnload(flip_cmd_read(0, 0)),
    #                                     call_dfu_upload(1),
    #                                     CALL_GET_STATUS])

    # def test_is_secured_select_memory_unit_outofrange(self):
    #     self.mock_usb.ctrl_transfer.side_effect = [usb.core.USBError("Error msg"), RSP_STATUS_OUTOFRANGE]

    #     flip = FlipProtocol(VID, PID, 1)

    #     status, secured_rsp = flip.is_secured()

    #     self.assertEqual('STATUS_OUTOFRANGE', status)
    #     self.assertIsNone(secured_rsp)

    #     self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x02)), CALL_GET_STATUS])

    # def test_is_secured_read_mem_unknown(self):
    #     self.mock_usb.ctrl_transfer.side_effect = [None,
    #                                                RSP_STATUS_OK,
    #                                                usb.core.USBError("Error msg"),
    #                                                RSP_STATUS_MEM_UNKNOWN]

    #     flip = FlipProtocol(VID, PID, 1)

    #     status, secured_rsp = flip.is_secured()

    #     self.assertEqual('STATUS_MEM_UNKNOWN', status)
    #     self.assertIsNone(secured_rsp)

    #     self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x02)),
    #                                     CALL_GET_STATUS,
    #                                     call_dfu_dnload(flip_cmd_read(0, 0)),
    #                                     CALL_GET_STATUS])

    # def test_is_secured_mem_protected(self):
    #     self.mock_usb.ctrl_transfer.side_effect = [None,
    #                                                RSP_STATUS_OK,
    #                                                None,
    #                                                usb.core.USBError("Error msg"),
    #                                                RSP_STATUS_MEM_PROTECTED]

    #     flip = FlipProtocol(VID, PID, 1)

    #     status, secured_rsp = flip.is_secured()

    #     self.assertEqual('STATUS_MEM_PROTECTED', status)
    #     self.assertIsNone(secured_rsp)

    #     self.mock_usb.assert_has_calls([call_dfu_dnload(flip_cmd_select_memory_unit(0x02)),
    #                                     CALL_GET_STATUS,
    #                                     call_dfu_dnload(flip_cmd_read(0, 0)),
    #                                     call_dfu_upload(1),
    #                                     CALL_GET_STATUS])


if __name__ == '__main__':
    unittest.main()
