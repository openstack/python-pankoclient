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
                            metavar='<KEY1=VALUE1;KEY2=VALUE2...>',
                            type=self.split_filter_param,
                            action='append',
                            help='Filter parameters to apply on'
                                 ' returned events.')
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
        columns = ('event_type', 'generated', 'message_id', 'traits')
        formatters = {'traits': lambda s: json.dumps(s, indent=4)}
        return (columns,
                (utils.get_item_properties(
                    s, columns, formatters=formatters) for s in events))


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
