The OSC CLI plugins
===================

This program provides a set of event related commands which are performed by
 OSC `openstack program`_. The `OpenStackClient`_ project provide a plugin
mechanism which supports loading other external projects' commands from
clients library entry points.

The event related commands begin with `openstack event` in `openstack`
command tool.

To configure the environment variables, see `openstack program`_.

.. _OpenStackClient: https://docs.openstack.org/python-openstackclient/latest/
.. _openstack program: https://docs.openstack.org/python-openstackclient/latest/cli/man/openstack.html

Examples
--------

List the capabilities of event interfaces::

  openstack event capabilities list

List the events::

  openstack event list

Show an event::

  openstack event show <MESSAGE_ID>

List event types::

  openstack event type list

List trait values of a specified event type and a trait name::

  openstack event traits list <EVENT_TYPE> <TRAIT_NAME>

List traits definitions for a specified event type::

  openstack event trait description <EVENT_TYPE>
