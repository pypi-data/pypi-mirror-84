"""
DFU protocol implementation according to USB DFU Bootloader Datasheet (doc7618)
"""
import sys
import time
from logging import getLogger
import usb.core

# USB timeout in milliseconds
DEFAULT_USB_TIMEOUT_MS = 5000

class DfuUsbDevice(object):
    """
    Class wrapping the USB level of a DFU device
    """

    def __init__(self):
        self.logger = getLogger(__name__)
        # Try to build a stack
        try:
            usb.core.find()
        except usb.core.NoBackendError:
            self.logger.error(
                "Unable to find backend USB driver for PyUSB!\n"
                "Install USB backend (eg: brew install libusb) and try again.")
            sys.exit(-1)

    def is_available(self, vid, pid):
        """
        Checks if a vid/pid combination is there

        :param vid: vendor id (USB)
        :param pid: product id (USB)
        :return:
        """
        target = "{0:x}:{1:x}".format(vid, pid)
        self.logger.info("Looking for usb device '%s'", target)
        devices = usb.core.show_devices()
        if target in devices:
            self.logger.info("Found")
            return True

        self.logger.info("device '%s' not found... ", target)
        return False

    def connect(self, vid, pid):
        """
        Connect to a given vid/pid

        :param vid: vendor id
        :param pid: product id
        :return: device object
        """
        self.logger.info("Connecting...")
        # Assume only one device.  Find will return the first one that matches.
        # DFU devices usually does not have unique serial numbers so no point in supporting match on serial number
        device = usb.core.find(idProduct=pid, idVendor=vid)

        if device is None:
            raise IOError("Unable to connect!")

        self.logger.info("Connected to device")
        self.logger.debug(str(device))

        # Assume only one configuration
        device.set_configuration()
        return device


class DfuProtocol(object):
    """ DFU (for FLIP) protocol class """

    # DFU commands
    DFU_CMD_DETACH = 0
    DFU_CMD_DNLOAD = 1
    DFU_CMD_UPLOAD = 2
    DFU_CMD_GETSTATUS = 3
    DFU_CMD_CLRSTATUS = 4
    DFU_CMD_GETSTATE = 5
    DFU_CMD_ABORT = 6

    # bmRequestType
    REQUEST_IN = 0xA1
    REQUEST_OUT = 0x21

    # Assuming only one interface
    DFU_INTERFACE = 0

    DFU_STATUS = {
        0x00: 'OK',
        0x01: 'ERROR_TARGET',
        0x02: 'ERROR_FILE',
        0x03: 'ERROR_WRITE',
        0x04: 'ERROR_ERASE',
        0x05: 'ERROR_CHECK_ERASED',
        0x06: 'ERROR_PROGRAMMING',
        0x07: 'ERROR_VERIFY',
        0x08: 'ERROR_ADDRESS',
        0x09: 'ERROR_NOT_DONE',
        0x0A: 'ERROR_FIRMWARE',
        0x0B: 'ERROR_VENDOR',
        0x0C: 'ERROR_USB_REQUEST',
        0x0D: 'ERROR_POWER_ON_RESET',
        0x0E: 'ERROR_UNKNOWN',
        0x0F: 'ERROR_STALLED_PACKET'
    }

    # Reverse the dict so we can look up its keys from values
    DFU_STATUS_INV = {v: k for k, v in DFU_STATUS.items()}

    DFU_STATUS_OK = DFU_STATUS_INV['OK']
    DFU_STATUS_ERR_TARGET = DFU_STATUS_INV['ERROR_TARGET']
    DFU_STATUS_ERR_FILE = DFU_STATUS_INV['ERROR_FILE']
    DFU_STATUS_ERR_WRITE = DFU_STATUS_INV['ERROR_WRITE']
    DFU_STATUS_ERR_ERASE = DFU_STATUS_INV['ERROR_ERASE']
    DFU_STATUS_ERR_CHECK_ERASED = DFU_STATUS_INV['ERROR_CHECK_ERASED']
    DFU_STATUS_ERR_PROGRAMMING = DFU_STATUS_INV['ERROR_PROGRAMMING']
    DFU_STATUS_ERR_VERIFY = DFU_STATUS_INV['ERROR_VERIFY']
    DFU_STATUS_ERR_ADDRESS = DFU_STATUS_INV['ERROR_ADDRESS']
    DFU_STATUS_ERR_NOT_DONE = DFU_STATUS_INV['ERROR_NOT_DONE']
    DFU_STATUS_ERR_FIRMWARE = DFU_STATUS_INV['ERROR_FIRMWARE']
    DFU_STATUS_ERR_VENDOR = DFU_STATUS_INV['ERROR_VENDOR']
    DFU_STATUS_ERR_USB_REQUEST = DFU_STATUS_INV['ERROR_USB_REQUEST']
    DFU_STATUS_ERR_POWER_ON_RESET = DFU_STATUS_INV['ERROR_POWER_ON_RESET']
    DFU_STATUS_ERR_UNKNOWN = DFU_STATUS_INV['ERROR_UNKNOWN']
    DFU_STATUS_ERR_STALLED_PACKET = DFU_STATUS_INV['ERROR_STALLED_PACKET']

    DFU_STATE = {
        0x00: 'APP_IDLE',
        0x01: 'APP_DETACH',
        0x02: 'IDLE',
        0x03: 'DOWNLOAD_SYNC',
        0x04: 'DOWNLOAD_BUSY',
        0x05: 'DOWNLOAD_IDLE',
        0x06: 'MANIFEST_SYNC',
        0x07: 'MANIFEST',
        0x08: 'MANIFEST_WAIT_RESET',
        0x09: 'UPLOAD_IDLE',
        0x0A: 'ERROR'
    }

    # Reverse the dict so we can look up its keys from values
    DFU_STATE_INV = {v: k for k, v in DFU_STATE.items()}

    DFU_STATE_APP_IDLE = DFU_STATE_INV['APP_IDLE']
    DFU_STATE_APP_DETACH = DFU_STATE_INV['APP_DETACH']
    DFU_STATE_IDLE = DFU_STATE_INV['IDLE']
    DFU_STATE_DOWNLOAD_SYNC = DFU_STATE_INV['DOWNLOAD_SYNC']
    DFU_STATE_DOWNLOAD_BUSY = DFU_STATE_INV['DOWNLOAD_BUSY']
    DFU_STATE_DOWNLOAD_IDLE = DFU_STATE_INV['DOWNLOAD_IDLE']
    DFU_STATE_MANIFEST_SYNC = DFU_STATE_INV['MANIFEST_SYNC']
    DFU_STATE_MANIFEST = DFU_STATE_INV['MANIFEST']
    DFU_STATE_MANIFEST_WAIT_RESET = DFU_STATE_INV['MANIFEST_WAIT_RESET']
    DFU_STATE_UPLOAD_IDLE = DFU_STATE_INV['UPLOAD_IDLE']
    DFU_STATE_ERROR = DFU_STATE_INV['ERROR']


    def __init__(self, vid, pid, timeout_s):
        """
        :param vid: Vendor ID (USB) of device to connect to
        :param pid: Product ID (USB) of device to connect to
        :param timeout_s: Timeout, in seconds, when attempting to connect to DFU device
        """
        self.logger = getLogger(__name__)

        self.dfu_device = DfuUsbDevice()

        while True:
            if self.dfu_device.is_available(vid, pid):
                break
            self.logger.info("Waiting for device...")
            time.sleep(1)
            timeout_s -= 1
            if timeout_s <= 0:
                raise IOError("Unable to connect to DFU")
        self.device = self.dfu_device.connect(vid, pid)

    def get_status(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Read status from device

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: dictionary with fields according to AVR4023
        """
        self.logger.debug("Read device status...")
        rsp = self.device.ctrl_transfer(
            self.REQUEST_IN, self.DFU_CMD_GETSTATUS, 0, self.DFU_INTERFACE, 6, usb_timeout_ms)
        status = {}
        status['bStatus'] = rsp[0]
        self.logger.debug("bStatus: %s", self.DFU_STATUS[rsp[0]])
        bwpolltimeout = ((rsp[3] << 16) & 0xFF0000) | ((rsp[2] << 8) & 0xFF00) | (rsp[1] & 0xFF)
        status['bwPollTimeOut'] = bwpolltimeout
        self.logger.debug("bwPollTimeOut: 0x%06X", bwpolltimeout)
        status['bState'] = rsp[4]
        self.logger.debug("bState: %s", self.DFU_STATE[rsp[4]])
        status['iString'] = rsp[5]
        self.logger.debug("iString: 0x%02X", rsp[5])  # Vendor specific

        return status

    def clear_status(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Clear device status

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        """
        self.logger.debug("Clear device status...")
        self.device.ctrl_transfer(self.REQUEST_OUT, self.DFU_CMD_CLRSTATUS, 0, self.DFU_INTERFACE, None, usb_timeout_ms)

    def abort(self, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        Abort command to reset DFU state machine to IDLE state

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        """
        self.logger.debug("Abort...")
        self.device.ctrl_transfer(self.REQUEST_OUT, self.DFU_CMD_ABORT, 0, self.DFU_INTERFACE, None, usb_timeout_ms)

    def download(self, data, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        DFU download setup request

        :param data: Bytes to download to device, either as a list, a bytes-like object, or iterable over elements
            of type byte
        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: True if OK, False if error occurred
        """
        self.logger.debug("Download setup request...")
        self.logger.debug("Download data: %s", str(data))

        try:
            self.device.ctrl_transfer(
                self.REQUEST_OUT, self.DFU_CMD_DNLOAD, 0, self.DFU_INTERFACE, data, usb_timeout_ms)
        except usb.core.USBError as error:
            # Catch, but ignore USBError.  Later get_status requests will give better feedback
            self.logger.debug("USBError (download): %s", error)
            return False

        return True

    def upload(self, num_bytes, usb_timeout_ms=DEFAULT_USB_TIMEOUT_MS):
        """
        DFU upload setup request

        :param usb_timeout_ms: Timeout in milliseconds for USB transfers
        :return: array of bytes received from device
        """
        self.logger.debug("Upload setup request...")

        try:
            return self.device.ctrl_transfer(
                self.REQUEST_IN, self.DFU_CMD_UPLOAD, 0, self.DFU_INTERFACE, num_bytes, usb_timeout_ms)
        except usb.core.USBError as error:
            # Catch, but ignore USBError.  Later get_status requests will give better feedback
            self.logger.warning("USBError (upload): %s Returning None from dfuprotocol.upload", error)
            return None
