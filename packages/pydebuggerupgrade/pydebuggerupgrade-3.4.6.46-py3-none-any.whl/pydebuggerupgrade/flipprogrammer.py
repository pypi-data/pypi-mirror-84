"""
Flip/DFU Programmer
"""
from logging import getLogger
from array import array

from .flipprotocol import FlipProtocol
from .dfuprotocol import DEFAULT_USB_TIMEOUT_MS
from .hexutils import parse_hex

# FLIP addresses are 16-bits so paging is needed.
FLIP_PAGE_SIZE = 64*1024

DEFAULT_WRITE_BUFFER_SIZE = 2048
DEFAULT_READ_BUFFER_SIZE = 1024
DEFAULT_FLASH_WRITE_ENTITY = 64

class FlipProgrammer(object):
    """
    Utility class providing functions to communicate with DFU/FLIP bootloaders
    """

    def __init__(self, vid, pid, timeout_s=5):
        """
        :param vid: Vendor ID (USB) of device to connect to
        :param pid: Product ID (USB) of device to connect to
        """
        self._write_buffer_size = DEFAULT_WRITE_BUFFER_SIZE
        self._read_buffer_size = DEFAULT_READ_BUFFER_SIZE
        self._flash_write_entity = DEFAULT_FLASH_WRITE_ENTITY
        self.logger = getLogger(__name__)
        self.flip = FlipProtocol(vid, pid, timeout_s)

    @property
    def read_buffer_size(self):
        """
        Max number of bytes that can be read from device in one go
        """
        return self._read_buffer_size

    @read_buffer_size.setter
    def read_buffer_size(self, read_buffer_size):
        if read_buffer_size <= 0:
            raise ValueError("Read buffer size must be greater than 0")
        self._read_buffer_size = read_buffer_size

    @property
    def write_buffer_size(self):
        """
        Max number of bytes the device can accept in one go when writing data to device
        """
        return self._write_buffer_size

    @write_buffer_size.setter
    def write_buffer_size(self, write_buffer_size):
        if write_buffer_size <= 0:
            raise ValueError("write_buffer_size must be greater than 0")
        if write_buffer_size < self._flash_write_entity:
            raise ValueError("write_buffer_size must at least be as big as the flash_write_entity")
        self._write_buffer_size = write_buffer_size

    @property
    def flash_write_entity(self):
        """
        Write entity for flash memory unit (bytes).

        From FLIP spec: <In order to be in accordance with the memory write entity (page size),
        X nonsignificant bytes may be added before the first byte to program. The X number is
        calculated to align the beginning of the firmware with the memory write entity.>
        So write entity is only for padding/alignment not for limiting number of bytes in each write
        """
        return self._flash_write_entity

    @flash_write_entity.setter
    def flash_write_entity(self, flash_write_entity):
        if flash_write_entity <= 0:
            raise ValueError("Flash write entity must be greater than 0")
        self._flash_write_entity = flash_write_entity

    def check_status_log(self, status, errormessage):
        """
        Checks FLIP status and logs the status

        :param status: FLIP status to check
        :param errormessage: Message to log when status is not OK
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if status is OK
        """
        if self.flip.status_is_ok(status):
            self.logger.debug("OK!")
            return True

        self.logger.error("%s FLIP status: %s", errormessage, status)
        return False

    def chip_erase(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Erase the target device

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Chip erase...")
        return self.check_status_log(self.flip.chip_erase(usb_timeout_ms=usb_timeout_ms), "Chip erase failed!")

    def blank_check_flash(self, start_address, end_address, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Runs blank check command to check specified address range for successful erase

        :param start_address: Start address for blank check
        :param end_address: End address for blank check (the blank check includes this address)
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Blank check from 0x{:X} to 0x{:X}".format(start_address, end_address))

        self.logger.info("Selecting memory unit FLASH...")
        if (not self.check_status_log(self.flip.select_memory_unit(FlipProtocol.MEMORY_UNIT_FLASH,
                                                                   usb_timeout_ms=usb_timeout_ms),
                                      "Selecting memory unit failed!")):
            return False

        while start_address <= end_address:
            # FLIP "page" size is 64KB
            page = start_address // FLIP_PAGE_SIZE
            self.logger.info("Selecting FLIP page %d...", page)
            if not self.check_status_log(self.flip.select_page(page, usb_timeout_ms=usb_timeout_ms),
                                         "Selecting page failed!"):
                return False
            # Since addresses starts at 0 the last address in a page is FLIP_PAGE_SIZE - 1.
            if (page*FLIP_PAGE_SIZE + FLIP_PAGE_SIZE - 1) < end_address:
                # The blank check address range exceeds or at least includes the complete current FLIP page
                end_page_address = 0xFFFF
            else:
                end_page_address = end_address % FLIP_PAGE_SIZE
            start_page_address = start_address % FLIP_PAGE_SIZE
            self.logger.info("Blank check from FLIP page address 0x{:X} to 0x{:X}...".format(start_page_address,
                                                                                             end_page_address))
            if not self.check_status_log(self.flip.blank_check(start_page_address, end_page_address,
                                                               usb_timeout_ms=usb_timeout_ms), "Blank check failed!"):
                return False

            start_address += (end_page_address - start_page_address + 1)

        return True

    def get_device_info(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Reads out various device info as device IDs, Bootloader version, Bootloader IDs

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, device_info
            status: True if OK, False if error occurred
            device_info: Dictionary of device info
        """
        self.logger.info("Reading device info...")

        status, device_ids = self.flip.get_device_ids(usb_timeout_ms=usb_timeout_ms)

        if self.flip.status_is_ok(status):
            self.logger.info("Device IDs:")
            idstring = ""
            for key in device_ids:
                if idstring != "":
                    idstring += ", "
                idstring += key + " = " + "0x{:02X}".format(device_ids[key])
            self.logger.info(idstring)
        else:
            self.logger.error("Reading device IDs failed! FLIP status: %s", status)
            return False, None

        status, bootloader_ids = self.flip.get_bootloader_ids(usb_timeout_ms=usb_timeout_ms)

        if self.flip.status_is_ok(status):
            self.logger.info("Bootloader IDs:")
            idstring = ""
            for key in bootloader_ids:
                if idstring != "":
                    idstring += ", "
                idstring += key + " = " + "0x{:02X}".format(bootloader_ids[key])
            self.logger.info(idstring)
        else:
            self.logger.error("Reading bootloader IDs failed! FLIP status: %s", status)
            return False, None

        status, version = self.flip.get_bootloader_version(usb_timeout_ms=usb_timeout_ms)

        if self.flip.status_is_ok(status):
            self.logger.info("Bootloader version:")
            versionstring = ""
            for key in version:
                if versionstring != "":
                    versionstring += ", "
                versionstring += key + " = " + "0x{:02X}".format(version[key])
            self.logger.info(versionstring)
        else:
            self.logger.error("Reading bootloader version failed! FLIP status: %s", status)
            return False, None

        return True, {'device_ids': device_ids, 'bootloader_version': version, 'bootloader_ids': bootloader_ids}

    def program_flash_from_hex(self, hexfile, start_address=0, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Programs a hex file to target FLASH memory

        :param hexfile: Intel(R) Hex file containing data and address information
        :param start_address: Defines at which address to start writing the hexfile content to.
            Note that the start address in the hex file is overridden by this parameter.  Ususally the start_address
            parameter should be set to 0 as all FLIP memories start at address 0
        :param usb_timeout_ms Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Programming %s to FLASH...", hexfile)

        self.logger.info("Selecting memory unit FLASH...")
        if not self.check_status_log(self.flip.select_memory_unit(FlipProtocol.MEMORY_UNIT_FLASH,
                                                                  usb_timeout_ms=usb_timeout_ms),
                                     "Selecting memory unit failed!"):
            return False

        #pylint: disable=unused-variable
        start_address_hex, data = parse_hex(hexfile)

        written = 0
        current_flip_page = -1

        while written < len(data):
            flip_page = start_address // FLIP_PAGE_SIZE
            if current_flip_page != flip_page:
                self.logger.info("Selecting FLIP page %d...", flip_page)
                if not self.check_status_log(self.flip.select_page(flip_page, usb_timeout_ms=usb_timeout_ms),
                                             "Selecting page failed!"):
                    return False
                current_flip_page = flip_page

            # Addressing is relative to current FLIP page
            start_flip_page_address = start_address % FLIP_PAGE_SIZE

            # If start address is not aligned with memory write entity it will be padded to match start of write entity.
            # We have to take this padding into account when limiting number of bytes to match _write_buffer_size
            max_num_bytes = self._write_buffer_size - start_flip_page_address % self._flash_write_entity
            # Check if more than one full write buffer remains
            if (len(data) - written) > max_num_bytes:
                # Writing a full buffer as there is more than one buffer left of data
                end_flip_page_address = start_flip_page_address+max_num_bytes-1
            else:
                # Less than one buffer left
                end_flip_page_address = start_flip_page_address+len(data[written:])-1

            # Check if we have to switch FLIP page in the middle of the data
            if start_flip_page_address // FLIP_PAGE_SIZE != end_flip_page_address // FLIP_PAGE_SIZE:
                # Write to the end of the current FLIP page
                end_flip_page_address = FLIP_PAGE_SIZE - 1

            bytes_to_write = end_flip_page_address - start_flip_page_address + 1
            self.logger.debug("Programming %d bytes from address 0x%04X...", bytes_to_write, start_flip_page_address)
            status = self.flip.program_start(start_flip_page_address,
                                             data[written:(written+bytes_to_write)],
                                             self.flash_write_entity,
                                             usb_timeout_ms=usb_timeout_ms)

            if not self.check_status_log(status, "Writing failed!"):
                return False
            start_address += bytes_to_write
            written += bytes_to_write

        return True

    def read_flash(self, start_address, end_address, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read FLASH in specified memory range including end_address location

        :param start_address: Address to start reading from
        :param end_address: Address of last location to read
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: status, data
            status: True if OK, False if error occurred
            data: Array of bytes read (if status is False then data will be None)
        """
        self.logger.info("Reading FLASH from 0x{:X} to 0x{:X}...".format(start_address, end_address))

        self.logger.info("Selecting memory unit FLASH...")
        if not self.check_status_log(self.flip.select_memory_unit(FlipProtocol.MEMORY_UNIT_FLASH,
                                                                  usb_timeout_ms=usb_timeout_ms),
                                     "Selecting memory unit failed!"):
            return False, None

        read = 0
        current_flip_page = -1
        # Must add 1 since end_address is also read
        bytes_to_read = end_address - start_address + 1

        data = array('B')
        while read < bytes_to_read:
            flip_page = start_address // FLIP_PAGE_SIZE
            if current_flip_page != flip_page:
                self.logger.info("Selecting FLIP page %d...", flip_page)
                if not self.check_status_log(self.flip.select_page(flip_page, usb_timeout_ms=usb_timeout_ms),
                                             "Selecting page failed!"):
                    return False, None
                current_flip_page = flip_page

            # Addressing is relative to current FLIP page
            start_flip_page_address = start_address % FLIP_PAGE_SIZE

            # Check if more than one full read buffer remains
            if (bytes_to_read - read) > self._read_buffer_size:
                # Reading a full buffer as there is more than one buffer left of read
                end_flip_page_address = start_flip_page_address + self._read_buffer_size - 1
            else:
                # Less than one buffer left
                end_flip_page_address = start_flip_page_address + bytes_to_read - read - 1

            # Check if we have to switch FLIP page in the middle of the read
            if start_flip_page_address // FLIP_PAGE_SIZE != end_flip_page_address // FLIP_PAGE_SIZE:
                # Write to the end of the current FLIP page
                end_flip_page_address = FLIP_PAGE_SIZE - 1

            self.logger.info("Reading from address 0x{:04X} to address 0x{:04X}...".format(start_flip_page_address,
                                                                                           end_flip_page_address))
            status, data_frame = self.flip.read_memory(start_flip_page_address, end_flip_page_address,
                                                       usb_timeout_ms=usb_timeout_ms)

            if self.check_status_log(status, "Reading failed!"):
                data.extend(data_frame)
            else:
                return False, None
            start_address += end_flip_page_address - start_flip_page_address + 1
            read += end_flip_page_address - start_flip_page_address + 1

        return True, data

    def verify_flash_against_hex(self, hexfile, start_address=0, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Verifies target FLASH memory agains hex file content

        :param hexfile: Intel(R) Hex file containing data and address information
        :param start_address: Defines at which address to start the verification.
            Note that the start address in the hex file is overridden by this parameter.  Ususally the start_address
            parameter should be set to 0 as all FLIP memories start at address 0
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if flash and hex matches, else False
        """
        self.logger.info("Verifying FLASH against %s...", hexfile)

        #pylint: disable=unused-variable
        start_address_hex, data_hex = parse_hex(hexfile)

        # Remember end_address is also read so must subtract 1
        status, data_read = self.read_flash(start_address, start_address + len(data_hex) - 1,
                                            usb_timeout_ms=usb_timeout_ms)
        if not status:
            self.logger.error("Reading FLASH failed!")
            return False

        if data_read != data_hex:
            self.logger.error("Verification failed!")
            if len(data_hex) != len(data_read):
                self.logger.error("Mismatch in data amount, read %d bytes, expected %d bytes",
                                  len(data_read), len(data_hex))
                return False
            index = 0
            for byte in data_hex:
                if byte != data_read[index]:
                    self.logger.error("First mismatch at 0x{:X}; expected: 0x{:02X}, actual: 0x{:02X}"
                                      .format(index + start_address, byte, data_read[index]))
                    return False
                index += 1
            self.logger.error("Unknown error!")
            self.logger.error("Expected: ")
            self.logger.error(data_hex)
            self.logger.error("Actual: ")
            self.logger.error(data_read)
            return False

        self.logger.info("OK!")
        return True

    def start_application(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Start the target application

        Requirements:
        CRC must be in place before attempting to start application.
        Either application must contain CRC when programming or the crc_write function must be run.

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Running start application command...")

        return self.check_status_log(self.flip.start_application(usb_timeout_ms=usb_timeout_ms),
                                     "Start application failed!")

    def crc_write(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Calculate CRC of Flash content and write to last 4 bytes of Flash

        Requirements:
        Since no erase is done before writing the CRC the last 4 bytes of Flash must be erased
        (contain 0xFF) before running this command

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Running CRC write command...")

        return self.check_status_log(self.flip.crc_write(usb_timeout_ms=usb_timeout_ms), "CRC write failed!")

    def clear_status(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Runs clear status command which resets any error state in the device

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Running clear status command...")

        return self.check_status_log(self.flip.clear_status(usb_timeout_ms=usb_timeout_ms), "Clear status failed!")

    def abort(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Runs abort command which resets dfu state machine to IDLE state

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.info("Running abort command...")

        return self.check_status_log(self.flip.abort(usb_timeout_ms=usb_timeout_ms), "Abort FAILED!")
