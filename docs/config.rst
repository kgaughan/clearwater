This tool scans a set of servers to check any SSH keys deployed onto them,
generating a report listing the results of the scan.

Configuration
=============

It takes an INI file that lists a set of SSH keys and CIDR ranges. The
keys provided can be public keys, private keys, or simply fingerprints and
can be also be marked as blacklisted if they are not meant to be used
anywhere. The CIDR ranges can be specified as either 'lax' (meaning that
unknown keys are acceptable) or 'strict' (meaning unknown keys are
unacceptable). Either way, if a blacklisted is found, a record is included
in the report.

Keys
----

Key sections have their titles prefixed with 'key:', the rest of the title
being how the key is referred to elsewhere in the file. It consists of
three key/value pairs, of which one is entirely optional and of the
remaining two, at least one must be present.

The first of those is 'blacklist', which defaults to 'no' if not present.
It identifies whether the given key ought to be treated as blacklisted.

The other two are 'fingerprint' and 'key'. The former is the key's hex
fingerprint; the latter is the path of either the public or private key
(the two are differenciated by whether the filename ends in '.pub'). If
both are present, the fingerprint is used to verify the key file is
correct.

Here's an example of what a key section looks like::

    [key ops]
    blacklist=no
    fingerprint=00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF
    key=/home/fred/.ssh/is_rsa-ops

In the interests of security, it's strongly advised that you only use
fingerprints where possible.

Ranges
------

Range sections have their titles prefixed with 'range:',the rest of their
title being a list of comma-separated CIDR ranges.

The key/value pair 'strictness' can have the value 'lax' or 'strict'. If
not present in a section, it defaults to 'strict'.

The other key/value pairs in the section refer to keys and the users they
are allowed to connect to the machine as a certain user. The key in the
key/value pair is the full name of the key section in question. The value
is a comma-separated list of username.

Here's an example of what two range sections look like::

    ; App server boxes.
    [range 192.0.2.0/24 198.51.100.0/24]
    strict=yes
    key ops=root
    key deploy=app1 app2

    ; Customers with management plans.
    [range 203.0.113.0/24]
    strict=no
    key ops=root

Scanning
========

When scanning boxes in a range, it will attempt to use one of the
configured keys with root access to boxes in that range. If no key file is
listed in the configuration file, it must be specified when the tool is
ran. It then parses /etc/ssh/sshd_config for the property
`AuthorizedKeysFile` to get the name of the authorised keys files. Once it
has that, it gets the home folders of all the users on the system and
checks for the existence of any authorised keys files, checking the
fingerprints of the public keys within them with the expected
fingerprints. If any blacklisted keys (or unknown keys if the scan is
strict) are found, this is flagged in the report.

Future
======

Further checking may be done in future iterations. For instance, checking
that the list of ciphers doesn't include any known weak ciphers, checking
the value of PermitRootLogin, &c.
