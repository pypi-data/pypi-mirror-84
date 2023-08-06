

class PyBehrtechException(Exception):
    """Base exception used by this module."""
    pass


class JWTError(PyBehrtechException):
    """A request for the JWT failed"""

    def __init__(self, message):
        PyBehrtechException.__init__(self, message)


class PermissionsError(PyBehrtechException):
    """User of request doesn't have permissions"""

    def __init__(self, message):
        PyBehrtechException.__init__(self, message)


class QueryError(PyBehrtechException):
    """Request to endpoint is invalid or was built incorrectly"""

    def __init__(self, url, message):
        self.url = url
        PyBehrtechException.__init__(self, url, message)
