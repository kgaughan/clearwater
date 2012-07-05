"""
Support for parsing the configuration files used by clearwater.
"""

from IPy import IP
from clearwater import utils
from clearwater.exceptions import ParseError, NoSuchFile, BadFingerprint
from clearwater.keys import import_public_key, is_fingerprint, to_fingerprint


def parse_key_section(parser, section):
    """
    Extract a keys section from the config.
    """
    if not parser.has_any_of(section, ('fingerprint', 'key')):
        raise ParseError("Need fingerprint and/or key in '%s'" % section)
    blacklist = parser.getboolean_default(section, 'blacklist', False)
    fingerprint = parser.get_default(section, 'fingerprint', None)
    key = parser.get_default(section, 'key', None)
    return {'blacklist': blacklist, 'key': key, 'fingerprint': fingerprint}


def parse_range_section(parser, section):
    """
    Extract a range section from the config.
    """
    strict = parser.getboolean_default(section, 'strict', True)
    keys_users = {}
    for k, v in parser.options(section):
        if k.startswith('key '):
            users = set(utils.parse_items(v))
            for key in utils.parse_items(k)[1:]:
                if key not in keys_users:
                    keys_users[key] = users
                else:
                    keys_users[key] |= users
    return {'strict': strict, 'keys': keys_users}


def check_fingerprint(path, expected):
    """
    Assert that the given public key file has the expected fingerprint.
    """
    with open(path, 'r') as fh:
        fingerprint = to_fingerprint(import_public_key(fh.readline()))
        if fingerprint != expected:
            raise BadFingerprint(
                "Bad fingerprint in '%s': got '%s', expected '%s'" % (
                    path, fingerprint, expected))


def check_key_section(contents):
    """
    Check that the given key section is well-formed.
    """
    key = contents['key']
    fingerprint = contents['fingerprint']

    if fingerprint is not None and not is_fingerprint(fingerprint):
        raise BadFingerprint("Malformed fingerprint: '%s'" % fingerprint)

    if key is not None:
        if not utils.is_file(key):
            raise NoSuchFile(key)
        if fingerprint is not None:
            check_fingerprint(key, fingerprint)


def parse_scanner_config(parser):
    """
    Parse the config file for the scanner tool.
    """
    keys = {}
    ranges = []
    for section in parser.sections():
        if section.startswith('key '):
            _, key = section.split(' ', 1)
            key = key.strip()
            if key != '':
                keys[key] = parse_key_section(parser, section)
                check_key_section(keys[key])
        elif section.startswith('range '):
            ips = [IP(ip) for ip in utils.parse_items(section)[1:]]
            if len(ranges) > 0:
                contents = parse_range_section(parser, section)
                contents['ips'] = ips
                ranges.append(contents)
    return keys, ranges
