"""
Python debugger firmware upgrade utilitiy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pydebuggerupgrade is a combined Command Line Interface and library utility for
upgrading firmware on Microchip debuggers with DFU based bootloaders.

These tools are currently supported:
* PKOB nano (nEDBG): Embedded debugger found on kits

To use pydebuggerupgrade as a library for applications, the following usage patterns
can be used:

Configure the firmware request:
    >>> from pydebuggerupgrade.artifactprovider import ArtifactRequest
    >>> artifact_request = ArtifactRequest('nedbg', 'latest')

Instantiate backend:
    >>> from pydebuggerupgrade.backend import Backend
    >>> backend = Backend()

Fetch and unzip firmware:
    >>> upgrade_firmware = backend.resolve_and_fetch_firmware(artifact_request, 'tempfolder')

Find tool to upgrade:
    >>> matching_tools = backend.get_matching_tools('nedbg')
    >>> selected_tool = matching_tools[0]

Do the actual upgrade:
    >>> backend.upgrade_tool_from_hexfile(selected_tool.name, selected_tool.serialnumber, upgrade_firmware.hexfile)

Print the pydebuggerupgrade version:
    >>> from pydebuggerupgrade.version import VERSION as pydebuggerupgrade_version
    >>> print("pydebuggerupgrade version {}".format(pydebuggerupgrade_version))

Print the backend API version:
    >>> print("pydebuggerupgrade backend API version: {}".format(backend.get_api_version()))
"""
