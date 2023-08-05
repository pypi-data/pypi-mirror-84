"""
This file defines a dictionary with the tool information needed by pydebuggerupgrade
"""

SUPPORTED_TOOLS = {
    'nedbg': {
        'short_name': 'nedbg',
        'pid': 0x2FC0,
        'vid': 0x03EB,
        'usb_product_string': 'nedbg'
    },
    # Only special purpose DFU bootloader supported for Microchip internal test purposes
    'pickit4': {
        'short_name': 'pickit4',
        'pid': 0x2FC1,
        'vid': 0x03EB,
        'usb_product_string': 'MPLAB PICkit 4'
    },
    # Only special purpose DFU bootloader supported for Microchip internal test purposes
    'snap': {
        'short_name': 'snap',
        'pid': 0x2FC3,
        'vid': 0x03EB,
        'usb_product_string': 'MPLAB Snap'
    }
}
