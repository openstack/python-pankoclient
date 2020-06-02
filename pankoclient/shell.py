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

import logging
import os
import sys
import warnings

from cliff import app
from cliff import commandmanager
from keystoneauth1 import exceptions
from keystoneauth1 import loading

from pankoclient import __version__
from pankoclient import client
from pankoclient.v2 import capabilities_cli
from pankoclient.v2 import events_cli


class PankoCommandManager(commandmanager.CommandManager):
    SHELL_COMMANDS = {
        "event list": events_cli.EventList,
        "event show": events_cli.EventShow,
        "event type list": events_cli.EventTypeList,
        "event trait list": events_cli.EventTraitList,
        "event trait description": events_cli.EventTraitDescription,
        "capabilities list": capabilities_cli.CliCapabilitiesList,
    }

    def load_commands(self, namespace):
        for name, command_class in self.SHELL_COMMANDS.items():
            self.add_command(name, command_class)


class PankoShell(app.App):
    def __init__(self):
        super(PankoShell, self).__init__(
            description='Panko command line client',
            version=__version__,
            command_manager=PankoCommandManager(None),
            deferred_help=True,
        )

        self._client = None

    def build_option_parser(self, description, version):
        """Return an argparse option parser for this application.

        Subclasses may override this method to extend
        the parser with more global options.
        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        """
        parser = super(PankoShell, self).build_option_parser(description,
                                                             version)
        # Global arguments, one day this should go to keystoneauth1
        parser.add_argument(
            '--os-region-name',
            metavar='<auth-region-name>',
            dest='region_name',
            default=os.environ.get('OS_REGION_NAME'),
            help='Authentication region name (Env: OS_REGION_NAME)')
        parser.add_argument(
            '--os-interface',
            metavar='<interface>',
            dest='interface',
            choices=['admin', 'public', 'internal'],
            default=os.environ.get('OS_INTERFACE'),
            help='Select an interface type.'
                 ' Valid interface types: [admin, public, internal].'
                 ' (Env: OS_INTERFACE)')
        parser.add_argument(
            '--panko-api-version',
            default=os.environ.get('PANKO_API_VERSION', '2'),
            help='Defaults to env[PANKO_API_VERSION] or 2.')
        parser.add_argument(
            '--panko-endpoint',
            metavar='<endpoint>',
            dest='endpoint',
            default=os.environ.get('PANKO_ENDPOINT'),
            help='Aodh endpoint (Env: PANKO_ENDPOINT)')
        loading.register_session_argparse_arguments(parser=parser)
        loading.register_auth_argparse_arguments(
            parser=parser, argv=sys.argv, default="password")

        return parser

    @property
    def client(self):
        # NOTE(sileht): we lazy load the client to not
        # load/connect auth stuffs
        if self._client is None:
            if hasattr(self.options, "endpoint"):
                endpoint_override = self.options.endpoint
            else:
                endpoint_override = None
            auth_plugin = loading.load_auth_from_argparse_arguments(
                self.options)
            session = loading.load_session_from_argparse_arguments(
                self.options, auth=auth_plugin)

            self._client = client.Client(self.options.panko_api_version,
                                         session=session,
                                         interface=self.options.interface,
                                         region_name=self.options.region_name,
                                         endpoint_override=endpoint_override)
        return self._client

    def clean_up(self, cmd, result, err):
        if isinstance(err, exceptions.HttpError) and err.details:
            print(err.details, file=sys.stderr)

    def configure_logging(self):
        if self.options.debug:
            # --debug forces verbose_level 3
            # Set this here so cliff.app.configure_logging() can work
            self.options.verbose_level = 3

        super(PankoShell, self).configure_logging()
        root_logger = logging.getLogger('')

        # Set logging to the requested level
        if self.options.verbose_level == 0:
            # --quiet
            root_logger.setLevel(logging.ERROR)
            warnings.simplefilter("ignore")
        elif self.options.verbose_level == 1:
            # This is the default case, no --debug, --verbose or --quiet
            root_logger.setLevel(logging.WARNING)
            warnings.simplefilter("ignore")
        elif self.options.verbose_level == 2:
            # One --verbose
            root_logger.setLevel(logging.INFO)
            warnings.simplefilter("once")
        elif self.options.verbose_level >= 3:
            # Two or more --verbose
            root_logger.setLevel(logging.DEBUG)

        # Hide some useless message
        requests_log = logging.getLogger("requests")
        cliff_log = logging.getLogger('cliff')
        stevedore_log = logging.getLogger('stevedore')
        iso8601_log = logging.getLogger("iso8601")

        cliff_log.setLevel(logging.ERROR)
        stevedore_log.setLevel(logging.ERROR)
        iso8601_log.setLevel(logging.ERROR)

        if self.options.debug:
            requests_log.setLevel(logging.DEBUG)
        else:
            requests_log.setLevel(logging.ERROR)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return PankoShell().run(args)
