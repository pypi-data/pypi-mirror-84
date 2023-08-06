"""
Defines exception classes for semver.

.. code-block:

    VersionError:
    |
    +-- InvalidVersionError   <-- ValueError
    |
    +-- WrongVersionTypeError <-- TypeError

"""


class VersionError(BaseException):
    """
    Base class for all semver errors.
    """


class InvalidVersionError(VersionError, ValueError):
    """
    Raised when there is no valid semver version.
    """
    pass


class WrongVersionTypeError(VersionError, TypeError):
    """
    Raised when the type of allowed semver version is incompatible.
    """
    pass
