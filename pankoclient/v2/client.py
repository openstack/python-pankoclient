#   Copyright 2017 Huawei, Inc. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from pankoclient import client
from pankoclient.exceptions import ClientException
from pankoclient.v2 import capabilities
from pankoclient.v2 import events


class Client(object):
    """Client for the Panko v2 API

    :param string session: session
    :type session: :py:class:`keystoneauth.adapter.Adapter`
    """

    def __init__(self, session=None, service_type='event', **kwargs):
        """Initialize a new client for the Panko v2 API."""
        if session is None:
            raise ClientException(message='Session is required argument')
        self.http_client = client.SessionClient(
            session, service_type=service_type, **kwargs)
        self.capabilities = capabilities.CapabilitiesManager(self.http_client)
        self.event = events.EventManager(self.http_client)
        self.event_type = events.EventTypeManager(self.http_client)
        self.event_trait = events.EventTraitsManager(self.http_client)
        self.event_trait_description = events.EventTraitDescriptionManager(
            self.http_client)
