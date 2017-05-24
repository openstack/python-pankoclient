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
from pankoclient import utils


class Event(base.Resource):
    pass


class EventType(base.Resource):
    pass


class EventTrait(base.Resource):
    pass


class TraitDescription(base.Resource):
    pass


class EventManager(base.ManagerWithFind):
    resource_class = Event

    def list(self, filters=None, limit=None, marker=None, sorts=None):
        """Return all events matching the query filters.

        :param query: Filter arguments for which Events to return
        :param limit: Maximum number of samples to be returned.
        :param sorts: A pair of sort key and sort direction combined with ":"
        :param marker: The pagination query marker, message id of the last
                       item viewed
        """
        pagination = utils.get_pagination_options(limit, marker, sorts)
        filter_string = (utils.filtersdict_to_url(filters) if
                         filters else "")
        url = "v2/events"
        options = []
        if filter_string:
            options.append(filter_string)
        if pagination:
            options.append(pagination)
        if options:
            url += "?" + "&".join(options)
        return self._list(url)

    def get(self, message_id):
        """Return a single event with the given message id.

        :param message_id: Message ID of the Event to be returned
        """
        path = '/v2/events/%s'
        return self._get(path % message_id)


class EventTypeManager(base.ManagerWithFind):
    resource_class = EventType

    def list(self):
        url = '/v2/event_types/'
        return self._list(url)


class EventTraitsManager(base.ManagerWithFind):
    resource_class = EventTrait

    def list(self, event_type, trait_name):
        url = '/v2/event_types/%s/traits/%s' % (event_type, trait_name)
        return self._list(url)


class EventTraitDescriptionManager(base.ManagerWithFind):
    resource_class = TraitDescription

    def list(self, event_type):
        url = '/v2/event_types/%s/traits/' % event_type
        return self._list(url)
