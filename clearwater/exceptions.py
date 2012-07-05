"""
Exceptions thrown within clearwater.
"""


class ParseError(Exception):
    """
    A config file contains malformed data.i
    """
    pass


class NoSuchFile(Exception):
    """
    The given file could not be found.
    """
    pass


class BadFingerprint(Exception):
    """
    The given fingerprint is malformed or not consistent with the public key.
    """
    pass
