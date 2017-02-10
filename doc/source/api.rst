The :mod:`pankoclient` Python API
=================================

.. module:: pankoclient
   :synopsis: A client for the Panko API.

.. currentmodule:: pankoclient

Usage
-----

To use pankoclient in a project::

    >>> from pankoclient.v2 import client
    >>> panko = client.Client(...)
    >>> panko.event.list()

Reference
---------

For more information, see the reference:

.. toctree::
   :maxdepth: 2

   ref/v2/index

