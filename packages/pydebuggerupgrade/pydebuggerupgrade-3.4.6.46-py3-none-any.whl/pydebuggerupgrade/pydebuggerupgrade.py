"""
Command line utility for firmware upgrade of tools
"""
# Python 3 compatibility for Python 2
from __future__ import print_function

import sys
import os
import argparse
import logging
from logging.config import dictConfig
import textwrap
import yaml

from appdirs import user_log_dir
from yaml.scanner import ScannerError

# pydebuggerupgrade main function
from . import pydebuggerupgrade_main

def setup_logging(user_requested_level=logging.WARNING, default_path='logging.yaml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI
    """
    # Logging config YAML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the YAML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rt') as file:
                # Load logging configfile from yaml
                configfile = yaml.safe_load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Create it if it does not exist
                os.makedirs(logdir, exist_ok=True)
                # Look through all handlers, and prepend log directory to redirect all file loggers
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])

                # Console logging takes granularity argument from CLI user
                configfile['handlers']['console']['level'] = user_requested_level
                # Root logger must be the most verbose of the ALL YAML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except ScannerError:
            # Error while parsing YAML
            print("Error parsing logging config file '{}'".format(path))
        except KeyError as keyerror:
            # Error looking for custom fields in YAML
            print("Key {} not found in logging config file".format(keyerror))
    else:
        # Config specified by environment variable not found
        print("Unable to open logging config file '{}'".format(path))

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

# Entrypoint for installable CLI
def main():
    """
    Entrypoint
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
    Firmware upgrade utility for tools with DFU bootloader
    Can upgrade using firmware images from:
        - hex file by specifying its path
        - zip package by specifying its path
        - latest released firmware from the pack server by specifying "latest"
        - pack server by specifying the exact pack version (NB: not firmware version)
        - artifactory by specifying "continuous", "stable", "release" (Microchip internal only)
        - artifactory by specifying the exact artifact version (Microchip internal only)
    Pack server is located at: https://packs.download.microchip.com
            '''),
        epilog=textwrap.dedent('''\
    Usage examples:

        Upgrade PKOB nano (nEDBG) with hex
        - pydebuggerupgrade -t nedbg nedbg.hex

        Upgrade PKOB nano (nEDBG) with zip
        - pydebuggerupgrade -t nedbg nedbg_fw-1.13.458.zip

        Upgrade PKOB nano (nEDBG) with a specific pack version (not firmware version) from pack server
        - pydebuggerupgrade -t nedbg 1.0.33

        Upgrade PKOB nano (nEDBG) with firmware from the latest released pack
        - pydebuggerupgrade -t nedbg latest

        Upgrade PKOB nano (nEDBG) from artifact repository by status label (Microchip internal only)
        - pydebuggerupgrade -t nedbg -m release

        Upgrade PKOB nano (nEDBG) from artifact repository by version (Microchip internal only)
        - pydebuggerupgrade -t nedbg -m 1.16.507

            '''))

    parser.add_argument("firmware",
                        # This makes firmware argument optional only if version (-V/--version) argument is given
                        nargs="?" if "-V" in sys.argv or "--version" in sys.argv
                        or "-R"  in sys.argv or "--release-info" in sys.argv
                        or "-r"  in sys.argv or "--report" in sys.argv else None,
                        help="firmware image to program to tool")

    parser.add_argument("-t", "--tool",
                        type=str.lower,
                        help="tool to connect to, default is 'nedbg'",
                        default='nedbg')

    parser.add_argument("-a", "--all",
                        help="upgrade all tools matching the tool type and USB serial number",
                        action='store_true')

    parser.add_argument("-ab", "--allbootmode",
                        help="""
                        upgrade all tools matching the tool type that are already in boot mode before doing the upgrade
                        of the tool with the specified USB serial number
                        """,
                        action='store_true')

    parser.add_argument("-s", "--serialnumber",
                        type=str,
                        help="""
                        USB serial number of the unit to use.
                        Substring matching on end of USB serial number is supported
                        """)

    parser.add_argument("-v", "--verbose",
                        default="warning", choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="Logging verbosity level")

    parser.add_argument("-tm", "--timeout",
                        type=int,
                        help="timeout in seconds when attempting to connect to tool",
                        default=10)

    parser.add_argument("-r", "--report",
                        help="report firmware versions only",
                        action="store_true")

    parser.add_argument("-f", "--force",
                        help="force upgrade or downgrade (no version checking)",
                        action="store_true")

    parser.add_argument("-m", "--microchip",
                        help="use Microchip internal artifact server",
                        action="store_true")

    parser.add_argument("-V", "--version",
                        help="print pydebuggerupgrade version number and exit",
                        action="store_true")

    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print pydebuggerupgrade release details and exit")

    arguments = parser.parse_args()

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, arguments.verbose.upper()))

    return pydebuggerupgrade_main.pydebuggerupgrade(arguments)


if __name__ == "__main__":
    sys.exit(main())
