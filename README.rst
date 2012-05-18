
==========
Clearwater
==========

**Clearwater** is credentials management and deployment application. Think
of it as a multi-user password managment application.

It's intended for situations where you need to securely store credentials
which a number of people need access to a common set of credentials.

In addition, it is intended to do SSH public key deployment to servers.

Ideally, it will also have facilities for periodically programmatically
updating credentials, though in the meantime, I see it only sending or
displaying alerts.

For SSH key management, it will, most likely support two deployment
methods. First will be that the application itself will periodically check
and deploy new keys on the machines in its network. Second will be having
a key management daemon running on each of the managed machines, which
will wait on deployment requests from the central server and monitor any
`authorized_keys` files to prevent their modification.

Users in the system are assigned to *groups*. Machines are in turn
assigned to *clusters*. Users and groups can be assigned access to
clusters and individual machines. Additionally, access to credentials can
be assigned to individual users or whole groups. All credentials are kept
in an encrypted backing store. For the application to be able to access
the backing store, an administrative user will need to provide a private
key to allow decryption of the data.

.. vim:set et tw=74:
