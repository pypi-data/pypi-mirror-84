"""
Firmware upgrader for tools with DFU bootloader (e.g. PKOB nano (nEDBG) etc.)
"""
import os

from logging import getLogger

# pyedbglib dependencies
from pyedbglib.hidtransport.hidtransportfactory import hid_transport
from pyedbglib.protocols import housekeepingprotocol
from pyedbglib.protocols.jtagice3protocol import Jtagice3ResponseError

from .flipprogrammer import FlipProgrammer
from .hexutils import parse_hex
from .dfuprotocol import DfuUsbDevice
from .pydebuggerupgrade_errors import PydebuggerupgradeError

# Long timeout for commands that takes a long time like chiperase
LONG_USB_TIMEOUT_MS = 40000

class Upgrader(object):
    """
    Class capable of doing firmware upgrades of Microchip CMSIS-DAP tools with DFU/FLIP based bootloaders
    """
    def __init__(self):
        self.logger = getLogger(__name__)
        self.transport = None

    @staticmethod
    def is_any_tool_in_bootmode(vid, pid):
        """
        Returns true if any tool with the given VID and PID are already in boot mode
        """
        dfu_device = DfuUsbDevice()

        tool_in_bootmode = False
        if dfu_device.is_available(vid, pid):
            tool_in_bootmode = True

        del dfu_device

        return tool_in_bootmode

    def get_matching_tools(self, product, serialnumber_substring=''):
        """
        Get a list of all tools with a USB serial number ending with serialnumber_substring.
        """
        if self.transport is None:
            self.transport = hid_transport()

        return self.transport.get_matching_tools(serialnumber_substring, product)

    def tool_connect(self, product, serialnumber):
        """
        Attempt to connect to the HID interface to put the tool into upgrade mode

        :param serialnumber: USB serial number to connect to
        :param product: product to connect to

        raises PydebuggerupgradeError if tool connection fails
        """
        # Try to connect to tool
        if self.transport is None:
            self.transport = hid_transport()
        try:
            if not self.transport.connect(serialnumber, product):
                self.transport = None
        except IOError:
            self.transport = None

        # If an attempt to connect fails, transport will be None.
        # Either the device is not there, or perhaps its in upgrade mode already or
        # there are more than one tool matching the product and USB serial number.
        # Either way - there is nothing more to do here
        if self.transport is None:
            raise PydebuggerupgradeError("Tool connection failed")

    def tool_disconnect(self):
        """Shut down tool connection"""
        if self.transport is not None:
            self.transport.disconnect()
        self.take_down_transport()

    def take_down_transport(self):
        """Remove transport stack"""
        self.transport = None

    def get_current_version(self):
        """
        Retrieves the current firmware version from a connected device

        :param transport: hid transport object
        return: version information as string

        raises PydebuggerupgradeError if no tranport is connected
        """
        self._check_transport_raise()

        # Sign on
        housekeeping = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)
        housekeeping.start_session()

        # Read versions
        self.logger.info("Checking current version")
        versions = housekeeping.read_version_info()
        version_string = "{0:d}.{1:d}.{2:d}".format(versions['firmware_major'], versions['firmware_minor'],
                                                    versions['build'])

        self.logger.info("Firmware version %s detected", version_string)

        if int(versions['build']) == 0:
            self.logger.warning("WARNING! Build number ZERO detected!")
            self.logger.warning("Either this tool has no bootloader, or a locally built image is currently installed.")

        # Sign off
        housekeeping.end_session()
        return version_string

    def enter_upgrade_mode(self):
        """
        Enters upgrade mode

        raises Pydebuggerupgrade error if failed to enter upgrade mode
        """
        self._check_transport_raise()

        # Sign on
        housekeeping = housekeepingprotocol.Jtagice3HousekeepingProtocol(self.transport)

        # Collect version info
        #version = get_current_version(transport)
        housekeeping.start_session()
        self.logger.info("Enter upgrade mode...")
        try:
            housekeeping.enter_upgrade_mode()
        except Jtagice3ResponseError:
            raise PydebuggerupgradeError("Enter upgrade mode failed.")
        except IOError:
            # Benefit of the doubt, since USB is being torn down
            self.logger.warning("IOError enterring upgrade. Continuing.")

        # No end session
        del housekeeping
        self.transport = None

    def upgrade(self, vid, pid, app_hex, connect_timeout_s=10):
        """
        Do the actual firmware upgrade (erase, write, verify and start application)

        :param vid: USB Vendor ID of tool to upgrade
        :param pid: USB Product ID of tool to upgrade
        :param app_hex: name of hexfile with application
        :param connect_timeout_s: timeout in seconds when attempting to connect to the bootloader

        raises Pydebuggerupgrade error if failed to upgrade
        """
        self.logger.info("Upgrading with firmware: '%s'", app_hex)

        try:
            flip = FlipProgrammer(vid, pid, timeout_s=connect_timeout_s)
        except IOError as error:
            raise PydebuggerupgradeError(error)

        if flip is None:
            raise PydebuggerupgradeError("Unable to connect FLIP programmer")

        self._read_and_log_device_info(flip)

        self.logger.info("Performing chip erase")
        # Using long timeout since chip erase on some parts takes a long time
        status = flip.chip_erase(LONG_USB_TIMEOUT_MS)
        self._check_status_and_raise(status, "Chip erase")

        hexfile = os.path.normpath(app_hex)

        #pylint: disable=unused-variable
        startadr, data = parse_hex(hexfile)

        self.logger.info("Performing blank check from 0 to 0x%04X", len(data))
        status = flip.blank_check_flash(0, len(data) - 1)
        self._check_status_and_raise(status, "Blank check")

        self.logger.info("Programming %s", hexfile)
        status = flip.program_flash_from_hex(hexfile)
        self._check_status_and_raise(status, "Programming")

        self.logger.info("Verifying")
        status = flip.verify_flash_against_hex(hexfile)
        self._check_status_and_raise(status, "Verify")

        self.logger.info("Writing CRC")
        status = flip.crc_write()
        self._check_status_and_raise(status, "Writing CRC")

        self.logger.info("Starting application")
        status = flip.start_application()
        self._check_status_and_raise(status, "Starting application")

        del flip

        self.logger.info("Upgrade DONE!")

    def _check_status_and_raise(self, status, operation):
        if status:
            self.logger.info("%s OK!", operation)
        else:
            raise PydebuggerupgradeError("{} failed!".format(operation))

    def _read_and_log_device_info(self, flipprogrammer):
        self.logger.info("Reading device info")
        status, info = flipprogrammer.get_device_info()
        if status:
            for key in info:
                self.logger.debug("%s:", key)
                for innerkey in info[key]:
                    self.logger.debug('  %s=0x%02X} ', innerkey, info[key][innerkey])
        else:
            self.logger.error("Reading device info failed!")


    def _check_transport_raise(self):
        """
        Check if transport is connected and raise exception if it isn't
        """
        if not self.transport:
            raise PydebuggerupgradeError("No transport connected")
