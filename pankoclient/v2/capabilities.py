#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from pankoclient.common import base


class Capabilities(base.Resource):
    pass


class CapabilitiesManager(base.ManagerWithFind):
    resource_class = Capabilities

    def list(self):
        """List capabilities"""
        cap_url = "v2/capabilities/"
        return self._get(cap_url)
