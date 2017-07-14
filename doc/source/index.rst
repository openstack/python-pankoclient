.. pankoclient documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python bindings to the Panko API
================================

This is a client for Panko API. There's :doc:`a Python API
<api>` (the :mod:`pankoclient` module), and a set of event related commands
which are integrated with the OSC CLI tool. Each implements the entire Panko
API.

.. warning::

   This is a new client to interact with Panko API. There may be differences
   in functionality, syntax, and command line output when compared with the
   event functionality provided by ceilometerclient.


.. seealso::

    You may want to read the `Panko Developer Guide`__  -- the overview, at
    least -- to get an idea of the concepts. By understanding the concepts
    this library should make more sense.

    __ https://docs.openstack.org/panko/latest/


Contents:

.. toctree::
   :maxdepth: 2

   installation
   osc_integrated_commands
   api
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

