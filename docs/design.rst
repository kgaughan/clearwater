=====================================================
Design for Clearwater, a credential management system
=====================================================

Overview
========

**Clearwater** is intended to manage credentials for an organisation.

The credentials it will eventually be able to manage, in order of priority
are:

* Passwords
* SSH public keys
* TLS certificates
* One-Time Passwords

Clearwater is intended not to take shortcuts with how it manages credentials.
Any credentials stored backing store will encrypted with, by default at least,
AES in CTR mode, and stored with a HMAC of the result. Upon startup, a user
with administrative privileges will have to log in and provide a key for the
decryption of shared credentials. All password updates will be logged. The
master key will not be stored anywhere.

Similarly, the system should allow for user-specific credentials. These would
be encrypted using a user-specific key, not the master key.

Storage
=======

TBD. Database backed. It shouldn't be a requirement that the storage itself
be encrypted as the data will be encrypted, but it should be encouraged.

The storage backend should include history tracking to allow for auditing of
updates. There should also be the possibility of adding an expiration date to
credentials to allow allow for the notification of interested parties as to
when said credential should be regenerated.

Export
======

As some credentials might need to be exported into configuration files, there
ought to be a way to specify a template for doing so, including associating
additional information (asides from usernames and passwords) with the
credentials.

Programmatic access
===================

Where possible, it should be preferred that programs request specific
credentials from Clearwater rather than relying on a configuration file. Thus
Clearwater will need an API to allow access to this, more than likely JSON-RPC
based or RESTful.

As this means introducing what's essentially a single proint of failure into
systems, some mechanism of distribution will be needed to mitigate against
this.

Certificate distribution
========================

Partly independent of Clearwater will be agents that run on systems to
distribute things like certificates, &c.
