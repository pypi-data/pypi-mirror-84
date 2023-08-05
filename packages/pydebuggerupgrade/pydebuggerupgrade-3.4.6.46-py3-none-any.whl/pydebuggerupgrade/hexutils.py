"""
Hex file utilities
"""
import random
import os
from logging import getLogger
from intelhex import IntelHex


def parse_hex(filename):
    """
    Parse hex file and convert to raw binary data

    param filename: Path to file to be parsed
    return: start_address, data
        start_address: First address in hex file containing data
        data: Raw data from hex file
    """
    logger = getLogger(__name__)
    logger.info("Parsing %s...", filename)
    intelhex = IntelHex()
    intelhex.fromfile(filename, format='hex')
    data = intelhex.tobinarray()
    start_address = intelhex.minaddr()
    logger.info("File contained {} bytes starting at address 0x{:08X}".format(len(data), start_address))

    return start_address, data

def make_random_hex(filename, start_address, size):
    """
    Make Intel(R) hex file with random byte values

    param filename: File name/path to store the random hex file to
    param start_address: Start address to be written to the hex
    param size: Number of data bytes to include in the hex
    """
    filename = os.path.normpath(filename)
    filedir = os.path.dirname(filename)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    hexfile = IntelHex()
    # Add some random data to the hexfile
    for index in range(start_address, start_address + size):
        hexfile[index] = random.randint(0, 255)

    # Turn the hexfile object into an actual file
    hexfile.write_hex_file(filename)

def make_hex_with_value(filename, start_address, size, value):
    """
    Make Intel(R) hex file with given byte value

    param filename: File name/path to store the random hex file to
    param start_address: Start address to be written to the hex
    param size: Number of data bytes to include in the hex
    param value: Byte value to write to all locations
    """
    filename = os.path.normpath(filename)
    filedir = os.path.dirname(filename)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    hexfile = IntelHex()
    # Add some random data to the hexfile
    for index in range(start_address, start_address + size):
        hexfile[index] = value

    # Turn the hexfile object into an actual file
    hexfile.write_hex_file(filename)
