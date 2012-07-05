"""
Key file management.
"""

import base64
from collections import namedtuple
import hashlib
import re


FINGERPRINT = re.compile('^[0-9A-F]{2}(:[0-9A-F]{2}){15}$')


PublicKey = namedtuple('PublicKey', ('keytype', 'key', 'comment'))


def import_public_key(line):
    """
    Import a single public key.
    """
    keytype, key, comment = line.split(' ', 2)
    return PublicKey(
        keytype=keytype,
        key=base64.b64decode(key),
        comment=comment.strip())


def import_public_keys(fh):
    """
    Import a set of public keys from a file.
    """
    return [import_public_key(line) for line in fh.readlines()]


def add_colons(s):
    """
    Puts a colon after every second character in the input string.
    """
    return ':'.join(s[i:i + 2] for i in xrange(0, len(s), 2))


def to_fingerprint(public_key):
    """
    Convert a public key to its fingerprint.
    """
    return add_colons(hashlib.md5(public_key.key).hexdigest())


def is_fingerprint(fingerprint):
    """
    Checks if a key fingerprint is well-formed.
    """
    return FINGERPRINT.match(fingerprint) is not None
