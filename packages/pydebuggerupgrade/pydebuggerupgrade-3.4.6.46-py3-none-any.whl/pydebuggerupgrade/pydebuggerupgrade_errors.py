"""
pydebuggerupgrade specific errors
"""

class PydebuggerupgradeError(Exception):
    """
    Base class for all pydebuggerupgrade specific exceptions
    """
    def __init__(self, msg=None, code=0):
        super(PydebuggerupgradeError, self).__init__(msg)
        self.code = code

class PydebuggerupgradeNotSupportedError(Exception):
    """
    Signals that an attempted operation is not supported
    """
    def __init__(self, msg=None, code=0):
        super(PydebuggerupgradeNotSupportedError, self).__init__(msg)
        self.code = code
