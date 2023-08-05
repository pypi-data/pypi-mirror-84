"""
Firmware upgrade utility, main function
"""
import time

from .backend import Backend

try:
    from .version import VERSION, BUILD_DATE, COMMIT_ID
except ImportError:
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

# Timeout period when searching for matching tools after upgrading some tools
# already in upgrade mode to let them have time to re-enumerate
TIMEOUT_TOOL_SEARCH_S = 5

SUCCESS = 0
FAILURE = 1

def pydebuggerupgrade(args):
    """
    Main entry point (after argparsing)

    :param args: command line arguments
    """
    backend = Backend(args.timeout)

    if args.version or args.release_info:
        print("pydebuggerupgrade version {}".format(VERSION))
        if args.release_info:
            print("Build date: {}".format(BUILD_DATE))
            print("Commit ID:  {}".format(COMMIT_ID))
        return SUCCESS

    tool_name = args.tool

    supported_tools = backend.get_supported_tools()
    if tool_name not in supported_tools:
        print("Unsupported tool: '{}'".format(tool_name))
        supported_tools_string = ', '.join([str(item) for item in supported_tools])
        print("Only tools supported are: {}".format(supported_tools_string))
        return FAILURE

    # Normally there is no need to have retries when searching for matching tools as no tools have been rebooted yet
    timeout_tool_search_s = 1

    # First we check if any tools with matching VID and PID are already in boot mode.
    # When a tool is in boot mode there is no USB serial number available, only the VID and PID.
    # In other words it is not possible to separate two tools of the same type when both are in boot mode.
    if backend.is_any_tool_in_bootmode(tool_name):
        if args.all or args.allbootmode:
            status, new_version = backend.upgrade_from_source(source=args.firmware, tool_name=tool_name,
                                                              microchip_internal=args.microchip, boot_mode=True)
            if status:
                print("Upgrade (from boot mode) to version '{0:s}' successful".format(new_version))
                # After upgrade from boot mode, execution continues so that specific USB serial numbers can be addressed
            else:
                print("Upgrade from boot mode failed!")
                return FAILURE
            # Add a timeout to the search for matching tools as it might take some time until all tools
            # that were in upgrade mode upfront have re-enumerated after the upgrade
            timeout_tool_search_s = TIMEOUT_TOOL_SEARCH_S
        else:
            print("Detected tool already in boot mode")
            print("A tool in boot mode can't be separated from other tools of the same type.")
            print("To upgrade all tools already in boot mode use the -ab/--allbootmode option or "
                  "the -a/--all option.")
            return FAILURE

    status, matching_tools = _find_matching_tools(backend, args, timeout_tool_search_s)
    if status != SUCCESS:
        return status

    # Report only.  By -r or --report switch
    if args.report:
        # All tools
        print("Reporting firmware versions")
        if args.firmware:
            upgrade_candidate = backend.resolve_source_version(source=args.firmware, tool_name=args.tool,
                                                               microchip_internal=args.microchip)
            if upgrade_candidate:
                print("Upgrade candidate is version {0:s}".format(upgrade_candidate))
        for tool in matching_tools:
            current_version = backend.get_current_version(tool.name, tool.serialnumber)
            print("{0:s}:{1:s}={2:s}".format(tool.name, tool.serialnumber, current_version))
        return SUCCESS

    return_code = _upgrade_matching_tools(backend, args, matching_tools, source=args.firmware)
    return return_code

def _find_matching_tools(backend, args, timeout_s):
    tool_name = args.tool
    usb_serial = args.serialnumber
    matching_tools = None
    while timeout_s:
        matching_tools = backend.get_matching_tools(tool_name, usb_serial)
        if not matching_tools:
            # No matching tools found so wait a bit and do another attempt
            time.sleep(1)
            timeout_s -= 1
        else:
            # At least one matching tool was found so no need to retry
            break

    if len(matching_tools) > 1:
        if args.all:
            print("Finding all {0:s} tools (with USB serial number matching '{1:s}')"
                  .format(tool_name, usb_serial if usb_serial is not None else ''))
        else:
            if usb_serial:
                print("Too many {0:s} tools with USB serial number matching '{1:s}'".format(tool_name, usb_serial))
            else:
                print("Too many {0:s} tools".format(tool_name))
            for matching_tool in matching_tools:
                print("> {}".format(matching_tool.serialnumber))
            print("Use --all option to upgrade all of them")
            return FAILURE, []
    if not matching_tools:
        print("Found no {} tools with USB serial number matching '{}'".format(tool_name, usb_serial))
        if not (args.all or args.allbootmode):
            print("Tool could already be in upgrade mode, use the -ab/--allbootmode option to upgrade all tools "
                  "already in boot mode.")
        return FAILURE, []

    return SUCCESS, matching_tools

def _upgrade_matching_tools(backend, args, matching_tools, source):
    return_code = SUCCESS
    for tool in matching_tools:
        print("Upgrading {0:s} ({1:s}) to '{2:s}'".format(tool.name, tool.serialnumber, source))
        upgraded, new_version = backend.upgrade_from_source(source, tool_name=tool.name,
                                                            serialnumber=tool.serialnumber,
                                                            force=args.force,
                                                            microchip_internal=args.microchip)
        if upgraded:
            print("Upgrade to firmware version '{0:s}' successful".format(new_version))
        else:
            print("Upgrade skipped.  Current version is '{0:s}'  (use -f to force downgrade)".format(new_version))
    return return_code
