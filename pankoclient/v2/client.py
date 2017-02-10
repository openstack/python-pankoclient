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

from pankoclient.common import http
from pankoclient.v2 import events


class Client(object):
    """Client for the Panko v2 API."""

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Panko v1 API."""
        self.http_client = http._construct_http_client(*args, **kwargs)
        self.event = events.EventManager(
            self.http_client)
