from IPy import IP

from clearwater import config
from clearwater import utils


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
                keys[key] = config.parse_key_section(parser, section)
        elif section.startswith('range '):
            ips = [IP(ip) for ip in utils.parse_items(section)[1:]]
            if len(ranges) > 0:
                contents = config.parse_range_section(parser, section)
                contents['ips'] = ips
                ranges.append(contents)
    return keys, ranges
