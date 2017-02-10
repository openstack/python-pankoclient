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

from pankoclient.common import base
from pankoclient.common import utils

class Event(base.Resource):
    pass


class EventManager(base.ManagerWithFind):
    resource_class = Event

    def list(self, query=None, limit=None, marker=None, sorts=None):
        """List Events
        :param query: Filter arguments for which Events to return
        :type query: list
        :param limit: maximum number of resources to return
        :type limit: int
        :param marker: the last item of the previous page; we return the next
                       results after this value.
        :type marker: str
        :param sorts: list of resource attributes to order by.
        :type sorts: list of str
        """
        pagination = utils.get_pagination_options(limit, marker, sorts)
        #simple_query_string = EventManager.build_simple_query_string(query)

        url = self.url
        options = []
        if pagination:
            options.append(pagination)
        #if simple_query_string:
        #    options.append(simple_query_string)
        if options:
            url += "?" + "&".join(options)
        return self._get(url).json()
