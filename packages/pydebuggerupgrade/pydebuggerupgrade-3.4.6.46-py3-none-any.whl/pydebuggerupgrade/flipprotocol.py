"""
Implementation of FLIP protocol according to AVR4023 (AN_8457)

The FLIP protocol runs over a proprietary DFU USB protocol

The FLIP protocol uses 16-bit addresses which means that to support address spaces with more than 64k locations
a paging mechanism is needed. This is the reason for most address parameters containing "_page" in their name like
start_page_address or end_page_address. The addresses are then within one such 64KB page. The correct page must be
selected upfront with the select_page command.
"""
from logging import getLogger
from usb.core import USBError
from .dfuprotocol import DfuProtocol, DEFAULT_USB_TIMEOUT_MS

class FlipProtocol(object):
    """
    Implementation of the FLIP protocol according to AVR4023 (doc8457)
    """

    # According to the flip documentation (doc8457), the flip data packet should be 64 bytes long
    FLIP_PACKET_SIZE = 64

    # FLIP command groups
    CMD_GROUP_DOWNLOAD = 0x01
    CMD_GROUP_UPLOAD = 0x03
    CMD_GROUP_EXEC = 0x04
    CMD_GROUP_SELECT = 0x06

    # FLIP commands within each group
    # Group UPLOAD
    CMD_UPLOAD_READ_MEMORY = 0x00
    CMD_UPLOAD_BLANK_CHECK = 0x01
    # Group DOWNLOAD
    CMD_DOWNLOAD_PROGRAM_START = 0x00
    # Group SELECT
    CMD_SELECT_MEMORY = 0x03
    CMD_SELECT_MEMORY_UNIT = 0x00
    CMD_SELECT_MEMORY_PAGE = 0x01
    # Group EXEC
    CMD_EXEC_ERASE = 0x00
    CMD_EXEC_CRC_WRITE = 0x01
    CMD_EXEC_START_APP = 0x03
    CMD_EXEC_ERASE_CHIP = 0xFF

    # FLIP memory units
    MEMORY_UNIT_FLASH = 0x00
    MEMORY_UNIT_EEPROM = 0x01
    MEMORY_UNIT_SECURITY = 0x02
    MEMORY_UNIT_CONFIGURATION = 0x03
    MEMORY_UNIT_BOOTLOADER = 0x04
    MEMORY_UNIT_SIGNATURE = 0x05
    MEMORY_UNIT_USER = 0x06
    MEMORY_UNIT_INT_RAM = 0x07
    MEMORY_UNIT_EXT_MEM_CS0 = 0x08
    MEMORY_UNIT_EXT_MEM_CS1 = 0x09
    MEMORY_UNIT_EXT_MEM_CS2 = 0x0A
    MEMORY_UNIT_EXT_MEM_CS3 = 0x0B
    MEMORY_UNIT_EXT_MEM_CS4 = 0x0C
    MEMORY_UNIT_EXT_MEM_CS5 = 0x0D
    MEMORY_UNIT_EXT_MEM_CS6 = 0x0E
    MEMORY_UNIT_EXT_MEM_CS7 = 0x0F
    MEMORY_UNIT_EXT_MEM_DF = 0x10

    def __init__(self, vid, pid, timeout_s):
        """
        :param vid: Vendor ID (USB) of device to connect to
        :param pid: Product ID (USB) of device to connect to
        """
        self.logger = getLogger(__name__)
        self.dfu = DfuProtocol(vid, pid, timeout_s)
        self.status = 'STATUS_UNKNOWN'

    def get_status(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read status and convert to FLIP status

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP Status string
        """
        self.logger.debug("Reading device status...")

        dfu_status = self.dfu.get_status(usb_timeout_ms=usb_timeout_ms)

        if (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_OK and
                dfu_status['bState'] == DfuProtocol.DFU_STATE_IDLE):
            self.status = 'STATUS_OK'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_STALLED_PACKET and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_ERROR):
            self.status = 'STATUS_STALL'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_WRITE and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_ERROR):
            self.status = 'STATUS_MEM_UNKNOWN'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_WRITE and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_APP_IDLE):
            self.status = 'STATUS_MEM_PROTECTED'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_ADDRESS and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_ERROR):
            self.status = 'STATUS_OUTOFRANGE'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_CHECK_ERASED and
              (dfu_status['bState'] == DfuProtocol.DFU_STATE_APP_IDLE or
               dfu_status['bState'] == DfuProtocol.DFU_STATE_IDLE)):

        # Spec says dfu_status['bState'] == DFU_STATE_APP_IDLE but ATxmega128B1 and several other
        # implementations seems to answer with dfu_status['bState'] == DFU_STATE_IDLE when blank_check fails

            self.status = 'STATUS_BLANK_FAIL'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_NOT_DONE and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_DOWNLOAD_BUSY):
            self.status = 'STATUS_ERASE_ONGOING'
        elif (dfu_status['bStatus'] == DfuProtocol.DFU_STATUS_ERR_VERIFY and
              dfu_status['bState'] == DfuProtocol.DFU_STATE_ERROR):
            self.status = 'STATUS_VERIFICATION_ERROR'  # Typically CRC verification error upon starting application
        else:
            self.status = 'STATUS_UNKNOWN'

        self.logger.debug("FLIP status: %s", self.status)

        return self.status

    @staticmethod
    def status_is_ok(status):
        """
        Returns True if the provided FLIP status string indicates device is OK

        :param status: Status string to check
        :return True if status is OK
        """
        return status == 'STATUS_OK'

    def sign_on(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Connect to device and check status

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if everything is OK, False if error occurred
        """
        self.logger.debug("Signing on...")

        status = self.get_status(usb_timeout_ms=usb_timeout_ms)

        if not self.status_is_ok(status):
            self.logger.debug("DFU status not OK: %s, clearing status...", status)

            self.dfu.clear_status(usb_timeout_ms=usb_timeout_ms)

            status = self.get_status(usb_timeout_ms=usb_timeout_ms)

        return self.status_is_ok(status)

    def clear_status(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Resets the device status

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Clearing status...")
        self.dfu.clear_status(usb_timeout_ms=usb_timeout_ms)

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def abort(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Resets the DFU state machine to IDLE state

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("DFU abort...")
        self.dfu.abort(usb_timeout_ms=usb_timeout_ms)

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def get_device_ids(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read device ids

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, IDs
            status: FLIP status
            IDs: A dictionary of IDs
        """
        self.logger.debug("Reading device ids...")
        status = self.select_memory_unit(self.MEMORY_UNIT_SIGNATURE, usb_timeout_ms=usb_timeout_ms)

        if not self.status_is_ok(status):
            self.logger.warning("Reading device ids failed! Status after selecting memory unit: %s. Returning None",
                                status)
            return status, None

        status, id_data = self.read_memory(0, 3, usb_timeout_ms=usb_timeout_ms)

        self.logger.debug("Received data: %s", str(id_data))

        if not self.status_is_ok(status):
            self.logger.warning("Reading device ids failed! Status after read command: %s. Returning None", status)
            return status, None

        id_dict = {}

        id_dict['manufacturer'] = id_data[0]
        id_dict['family'] = id_data[1]
        id_dict['device'] = id_data[2]
        id_dict['revision'] = id_data[3]

        return status, id_dict

    def read_memory(self, start_page_address, end_page_address, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read memory from device

        :param start_page_address: 16-bit start page address. Refers to address within FLIP 64KB page
        :param end_page_address: 16-bit end page address. Refers to address within FLIP 64KB page
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, data
            status: FLIP status
            data: Array of byte values read from device
        """
        self.logger.debug("Reading from 0x{:02X} to 0x{:02X}...".format(start_page_address, end_page_address))
        command = [self.CMD_GROUP_UPLOAD, self.CMD_UPLOAD_READ_MEMORY, (start_page_address >> 8) & 0xFF,
                   start_page_address & 0xFF, (end_page_address >> 8) & 0xFF, end_page_address & 0xFF]

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("read_memory failed during dfu.download returning None. FLIP status: %s", status)
            return status, None
        data = self.dfu.upload(end_page_address - start_page_address + 1, usb_timeout_ms=usb_timeout_ms)

        return self.get_status(usb_timeout_ms=usb_timeout_ms), data

    def select_memory_unit(self, unit, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Select Flip memory unit

        :param unit: byte identifying memory unit according to AVR4023
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Selecting memory unit 0x{:02X}...".format(unit))
        command = [self.CMD_GROUP_SELECT, self.CMD_SELECT_MEMORY, self.CMD_SELECT_MEMORY_UNIT, unit & 0xFF, 0x00, 0x00]

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("select_memory_unit failed during dfu.download. FLIP status: %s", status)
            return status

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def chip_erase(self, retries=0, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Runs chip erase command until success or number of retries has been reached

        :param retries: Number of times to repeat the erase command waiting for the erase to complete
        :param retry_delay_ms: Number of milliseconds between each erase retry
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Performing chip erase...")
        command = [self.CMD_GROUP_EXEC, self.CMD_EXEC_ERASE, self.CMD_EXEC_ERASE_CHIP, 0x00, 0x00, 0x00]

        while True:
            self.dfu.download(command, usb_timeout_ms=usb_timeout_ms)
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            if self.status_is_ok(status):
                self.logger.debug("OK!")
                break
            if retries == 0:
                self.logger.warning("Chip erase failed! FLIP status: %s", status)
                break
            retries -= 1

        return status

    def blank_check(self, start_page_address, end_page_address, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Runs blank check command to check specified address range for successful erase

        :param start_page_address: 16-bit start page address.  Refers to address within FLIP 64KB page
        :param end_page_address: 16-bit end page address.  Refers to address within FLIP 64KB page
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Doing blank check...")
        command = [self.CMD_GROUP_UPLOAD, self.CMD_UPLOAD_BLANK_CHECK, (start_page_address >> 8) & 0xFF,
                   start_page_address & 0xFF, (end_page_address >> 8) & 0xFF, end_page_address & 0xFF]

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("blank_check failed during dfu.download. FLIP status: %s", status)
            return status

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def select_page(self, page, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Select FLIP page (64KB "pages" in FLIP)

        :param page: 16-bit page number.  Each FLIP page is 64KB
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Selecting page %d...", page)
        # MSB of page number sent first
        command = [self.CMD_GROUP_SELECT,
                   self.CMD_SELECT_MEMORY,
                   self.CMD_SELECT_MEMORY_PAGE,
                   (page >> 8) & 0XFF,
                   page & 0xFF,
                   0x00]

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("select_page failed during dfu.download. FLIP status: %s", status)
            return status

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def program_start(self, start_page_address, data, memory_write_entity=0,
                      usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Download data to device memory.

        Memory must be selected upfront with select_memory_unit.
        Addresses are FLIP page addresses not target page addresses.  A FLIP page is 64KB and the correct page must be
        selected upfront with the select_page command.
        :param start_page_address: 16-bit page start address.  Refers to address within FLIP 64KB page
        :param data: List of bytes to download to device memory
        :param memory_write_entity: Device memory write entity.  From the FLIP documentation (doc8457):
                "In order to be in accordance with the memory write entity (page size), X nonsignificant bytes may be
                added before the first byte to program. The X number is calculated to align the beginning of the
                firmware with the memory write entity."

                This statement indicates that the memory_write_entity equals the target page size. However at least
                for Xmega128B1 the bootloader uses the control endpoint size (64 bytes) as write_entity.
                In general the recommendation is to make sure the data and start_page_address is aligned with the
                target device memory page size.
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        # Note have to subtract one as the end address should point to the last address location to be written
        end_page_address = start_page_address + len(data) - 1
        self.logger.debug("Downlading data to address %d through %d...", start_page_address, end_page_address)

        # Addresses are sent MSB first
        command = [self.CMD_GROUP_DOWNLOAD, self.CMD_DOWNLOAD_PROGRAM_START, (start_page_address >> 8) & 0xFF,
                   start_page_address & 0xFF, (end_page_address >> 8) & 0xFF, end_page_address & 0xFF]

        # The FLIP command should be padded to 64 bytes before sending the data
        command.extend([0x00]*(self.FLIP_PACKET_SIZE - len(command)))

        # Align data with write_entity by padding with 0xFFs
        if memory_write_entity != 0:
            command.extend([0xFF]*(start_page_address % memory_write_entity))

        # And finally comes the data
        command.extend(data)

        # Note if FLIP version 1 support is going to be added we might need to add the DFU suffix,
        # see doc7618 USB DFU Bootloader Datasheet

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("program_start failed during dfu.download. FLIP status: %s", status)
            return status

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def get_bootloader_version(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read the major and minor bootloader versions

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, versions
            status: FLIP status
            versions: A dictionary of versions, None if reading versions failed
        """
        self.logger.debug("Reading bootloader versions...")
        status = self.select_memory_unit(self.MEMORY_UNIT_BOOTLOADER, usb_timeout_ms=usb_timeout_ms)

        if not self.status_is_ok(status):
            self.logger.warning("Reading bootloader versions failed! Status after selecting memory unit: %s. "
                                "Returning None", status)
            return status, None

        status, version_data = self.read_memory(0, 0, usb_timeout_ms=usb_timeout_ms)

        self.logger.debug("Received data: %s", str(version_data))

        if not self.status_is_ok(status):
            self.logger.warning("Reading bootloader versions failed! Status after read command: %s. "
                                "Returning None", status)
            return status, None

        version_dict = {}

        version_dict['major'] = (version_data[0] >> 4) & 0x0F
        version_dict['minor'] = version_data[0] & 0x0F

        return status, version_dict

    def get_bootloader_ids(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read the bootloader IDs

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, IDs
            status: FLIP status
            IDs: A dictionary of IDs
        """
        self.logger.debug("Reading bootloader IDs...")
        status = self.select_memory_unit(self.MEMORY_UNIT_BOOTLOADER, usb_timeout_ms=usb_timeout_ms)

        if not self.status_is_ok(status):
            self.logger.warning("Reading bootloader IDs failed! Status after selecting memory unit: %s. "
                                "Returning None", status)
            return status, None

        status, id_data = self.read_memory(1, 2, usb_timeout_ms=usb_timeout_ms)

        self.logger.debug("Received data: %s", str(id_data))

        if not self.status_is_ok(status):
            self.logger.warning("Reading bootloader IDs failed! Status after read command: %s. "
                                "Returning None", status)
            return status, None

        ids_dict = {}

        ids_dict['ID1'] = id_data[0]
        ids_dict['ID2'] = id_data[1]

        return status, ids_dict

    def crc_write(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Run CRC Write command (extension to Atmel FLIP protocol)

        This command calculates the CRC of the Flash memory unit and writes the CRC value to the last 4 bytes of
        Flash memory unit

        Requirements:
        The last 4 bytes of the Flash memory unit must contain 0xFF (must have been erased) before running this command

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Running CRC Write command...")

        command = [self.CMD_GROUP_EXEC, self.CMD_EXEC_CRC_WRITE, 0x00, 0x00, 0x00, 0x00]

        if not self.dfu.download(command, usb_timeout_ms=usb_timeout_ms):
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)
            self.logger.warning("CRC Write failed during dfu.download. FLIP status: %s", status)
            return status

        return self.get_status(usb_timeout_ms=usb_timeout_ms)

    def start_application(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Run Start Application command

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: FLIP status
        """
        self.logger.debug("Running Start Application command...")

        command = [self.CMD_GROUP_EXEC, self.CMD_EXEC_START_APP, 0x00, 0x00, 0x00, 0x00]

        self.dfu.download(command, usb_timeout_ms=usb_timeout_ms)

        try:
            status = self.get_status(usb_timeout_ms=usb_timeout_ms)

            # Need to send empty DFU_DOWNLOAD packet to do reset
            self.dfu.download([], usb_timeout_ms=usb_timeout_ms)

            return status
        except USBError:
            self.logger.warning("start_application failed to get status. This could be due to USB stack going down "
                                "when device is resetting.")
            return 'STATUS_OK'


    # MEMORY_UNIT_SECURITY not supported on at least some bootloaders (f.ex. ATxmega128B1).
    # Status MEM_PROTECTED will be returned when device is locked
    # def secure(self):

    # def is_secured(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
    #     """
    #     Check if device is secured

    #     :param usb_timeout_ms: Timeout in milliseconds for USB transfers
    #     :return: status, device_secured
    #       status: FLIP status
    #       device_secured: True if device is secured
    #     """
    #     self.logger.info("Checking if device is secured...")
    #     status = self.select_memory_unit(MEMORY_UNIT_SECURITY, usb_timeout_ms=usb_timeout_ms)

    #     if not self.status_is_ok(status):
    #         self.logger.warning("Checking if device is secured failed! Status after selecting memory unit: {}."
    #               "Returning None".format(status))
    #         return status, None

    #     status, secured = self.read_memory(0, 0, usb_timeout_ms=usb_timeout_ms)

    #     self.logger.debug("Received data: " + str(secured))

    #     if not self.status_is_ok(status):
    #         self.logger.warning("Checking if device is secured failed! Status after read command: {}. "
    #           "Returning None".format(status))
    #         return status, None

    #     return status, (secured[0] == 0x01)
