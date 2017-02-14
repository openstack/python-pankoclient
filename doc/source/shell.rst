The :program:`panko` shell utility
==================================

.. program:: panko
.. highlight:: bash

The :program:`panko` shell utility interacts with Panko API
from the command line.

You'll need to provide :program:`panko` with your OpenStack credentials.
You can do this with the :option:`--os-username`, :option:`--os-password`,
:option:`--os-tenant-id` and :option:`--os-auth-url` options, but it's easier to
just set them as environment variables:

.. envvar:: OS_USERNAME

    Your OpenStack username.

.. envvar:: OS_PASSWORD

    Your password.

.. envvar:: OS_TENANT_NAME

    Project to work on.

.. envvar:: OS_AUTH_URL

    The OpenStack auth server URL (keystone).

For example, in Bash you would use::

    export OS_USERNAME=user
    export OS_PASSWORD=pass
    export OS_TENANT_NAME=myproject
    export OS_AUTH_URL=http://auth.example.com:5000/v2.0

The command line tool will attempt to reauthenticate using your provided credentials
for every request. You can override this behavior by manually supplying an auth
token using :option:`--panko-endpoint` and :option:`--os-auth-token`. You can alternatively
set these environment variables::

    export PANKO_ENDPOINT=http://panko.example.org:8041
    export OS_AUTH_PLUGIN=token
    export OS_AUTH_TOKEN=3bcc3d3a03f44e3d8377f9247b0ad155

Also, if the server doesn't support authentication, you can provide
:option:`--os-auth-plugon` panko-noauth, :option:`--panko-endpoint`, :option:`--user-id`
and :option:`--project-id`. You can alternatively set these environment variables::

    export OS_AUTH_PLUGIN=panko-noauth
    export PANKO_ENDPOINT=http://panko.example.org:8041
    export PANKO_USER_ID=99aae-4dc2-4fbc-b5b8-9688c470d9cc
    export PANKO_PROJECT_ID=c8d27445-48af-457c-8e0d-1de7103eae1f

From there, all shell commands take the form::

    panko <command> [arguments...]

Run :program:`panko help` to get a full list of all possible commands,
and run :program:`panko help <command>` to get detailed help for that
command.

Examples
--------

#TODO
