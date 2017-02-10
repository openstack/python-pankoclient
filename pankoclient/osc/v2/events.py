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

import logging

from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
import six

from pankoclient.common.i18n import _

LOG = logging.getLogger(__name__)


class ListEvent(command.Lister):
    """List all baremetal servers"""

    def get_parser(self, prog_name):
        parser = super(ListEvent, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_("List additional fields in output")
        )
        parser.add_argument(
            '--all-projects',
            action='store_true',
            default=False,
            help=_("List the baremetal servers of all projects, "
                   "only available for admin users.")
        )
        return parser

    @staticmethod
    def _networks_formatter(network_info):
        return_info = []
        for port_uuid in network_info:
            port_ips = []
            for fixed_ip in network_info[port_uuid]['fixed_ips']:
                port_ips.append(fixed_ip['ip_address'])
            return_info.append(', '.join(port_ips))
        return '; '.join(return_info)

    def take_action(self, parsed_args):
        bc_client = self.app.client_manager.baremetal_compute

        if parsed_args.long:
            data = bc_client.server.list(detailed=True,
                                         all_projects=parsed_args.all_projects)
            formatters = {'network_info': self._networks_formatter}
            # This is the easiest way to change column headers
            column_headers = (
                "UUID",
                "Name",
                "Flavor",
                "Status",
                "Power State",
                "Image",
                "Description",
                "Availability Zone",
                "Networks"
            )
            columns = (
                "uuid",
                "name",
                "instance_type_uuid",
                "status",
                "power_state",
                "image_uuid",
                "description",
                "availability_zone",
                "network_info"
            )
        else:
            data = bc_client.server.list(all_projects=parsed_args.all_projects)
            formatters = None
            column_headers = (
                "UUID",
                "Name",
                "Status",
            )
            columns = (
                "uuid",
                "name",
                "status",
            )

        return (column_headers,
                (utils.get_item_properties(
                    s, columns, formatters=formatters
                ) for s in data))
