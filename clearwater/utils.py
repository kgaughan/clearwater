"""
A hodgepodge of stuff that fits nowhere else yet.
"""

import os.path
import ConfigParser as configparser


class ConfigParser(configparser.RawConfigParser):
    """
    A version of `ConfigParser.RawConfigParser` with convenience methods.
    """

    def has_any_of(self, section, options):
        """Ensure that at least one of the given options is present."""
        return any(self.has_option(section, option) for option in options)

    def get_default(self, section, option, default):
        """
        Version of `get()` that returns a default value rather than raising
        an exception if the options isn't present.
        """
        try:
            return self.get(section, option)
        except ValueError:
            return default

    def getboolean_default(self, section, option, default):
        """
        Version of `getboolean()` that returns a default value rather than
        raising an exception if the options isn't present.
        """
        try:
            return self.getboolean(section, option)
        except ValueError:
            return default


def parse_items(items):
    """Turn a space-separated list of items into a list."""
    return [item.strip() for item in items.split(' ') if item != '']


def is_file(path):
    """Does the given file exist?"""
    return os.path.isfile(os.path.realpath(path))
