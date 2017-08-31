#   Copyright 2016 Huawei, Inc. All rights reserved.
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

"""Panko v2 event action implementations"""
import copy

import json

from osc_lib.command import command
from osc_lib import utils


class EventList(command.Lister):
    """List events"""

    @staticmethod
    def split_filter_param(param):
        key, eq_op, value = param.partition('=')
        if not eq_op:
            msg = 'Malformed parameter(%s). Use the key=value format.' % param
            raise ValueError(msg)
        return key, value

    def get_parser(self, prog_name):
        parser = super(EventList, self).get_parser(prog_name)
        parser.add_argument('--filter', dest='filter',
                            metavar='<KEY>=<VALUE>',
                            type=self.split_filter_param,
                            action='append',
                            help='Filter parameters to apply on returned '
                                 'events. (can be applied multiple times)')
        parser.add_argument("--limit", type=int, metavar="<LIMIT>",
                            help="Number of events to return "
                                 "(Default is server default)")
        parser.add_argument("--marker", metavar="<MARKER>",
                            help="Last item of the previous listing. "
                                 "Return the next results after this value,"
                                 "the supported marker is message_id.")
        parser.add_argument("--sort", action="append",
                            metavar="<SORT_KEY:SORT_DIR>",
                            help="Sort of events attribute, "
                                 "e.g. name:asc")
        return parser

    def take_action(self, parsed_args):
        ac = self.app.client_manager.event
        filters = dict(parsed_args.filter) if parsed_args.filter else None
        events = ac.event.list(
            filters=filters, sorts=parsed_args.sort,
            limit=parsed_args.limit, marker=parsed_args.marker)
        columns = ('event_type', 'generated', 'message_id', 'traits:name',
                   'traits:value', 'traits:type')
        rows = []
        for event in events:
            traits_type = [t['type'] for t in event.traits]
            traits_name = [t['name'] for t in event.traits]
            traits_value = [t['value'] for t in event.traits]
            [getattr(event, item, '') for item in columns]
            row = (getattr(event, 'event_type', ''),
                   getattr(event, 'generated', ''),
                   getattr(event, 'message_id', ''),
                   '\n'.join(traits_name),
                   '\n'.join(traits_value),
                   '\n'.join(traits_type),)
            rows.append(row)
        return columns, tuple(rows)


class EventShow(command.ShowOne):
    """List events"""

    def get_parser(self, prog_name):
        parser = super(EventShow, self).get_parser(prog_name)
        parser.add_argument(
            'message_id',
            metavar='<message_id>',
            help="event of specified message_id to display"
        )
        return parser

    def take_action(self, parsed_args):
        ac = self.app.client_manager.event
        event = ac.event.get(message_id=parsed_args.message_id)
        data = copy.deepcopy(event._info)
        data.update({'traits': json.dumps(data['traits'], indent=4)})
        return self.dict2columns(data)


class EventTypeList(command.Lister):
    """List event types"""

    def take_action(self, parsed_args):
        ac = self.app.client_manager.event
        event_types = ac.event_type.list()
        return ('Event Type',), ((t,)for t in event_types)


class EventTraitList(command.Lister):
    """List event traits of a specified event type and trait name"""

    def get_parser(self, prog_name):
        parser = super(EventTraitList, self).get_parser(prog_name)
        parser.add_argument(
            'type_name',
            metavar='<EVENT_TYPE>',
            help='Type of the event for which traits will listed.'
        )
        parser.add_argument(
            'trait_name',
            metavar='<TRAIT_NAME>',
            help='The name of the trait to list.'
        )
        return parser

    def take_action(self, parsed_args):
        ac = self.app.client_manager.event
        event_traits = ac.event_trait.list(
            parsed_args.type_name, parsed_args.trait_name)
        columns = ('name', 'value', 'type')
        return (columns,
                (utils.get_item_properties(t, columns) for t in event_traits))


class EventTraitDescription(command.Lister):
    """List trait info for an event type."""

    def get_parser(self, prog_name):
        parser = super(EventTraitDescription, self).get_parser(prog_name)
        parser.add_argument(
            'type_name',
            metavar='<EVENT_TYPE>',
            help='Type of the event for which traits definitions will be '
                 'shown.'
        )
        return parser

    def take_action(self, parsed_args):
        ac = self.app.client_manager.event
        event_traits = ac.event_trait_description.list(parsed_args.type_name)
        columns = ('name', 'type')
        return (columns,
                (utils.get_item_properties(t, columns) for t in event_traits))
