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

import logging

from osc_lib import utils

from pankoclient.common.i18n import _

LOG = logging.getLogger(__name__)

DEFAULT_EVENT_API_VERSION = '2'
API_VERSION_OPTION = 'os_event_api_version'
API_NAME = 'event'
API_VERSIONS = {
    '2': 'pankoclient.v2.client.Client',
}


def make_client(instance):
    """Returns an event service client"""
    panko_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating event client: %s', panko_client)

    endpoint = instance.get_endpoint_for_service_type(
        API_NAME,
        region_name=instance.region_name,
        interface=instance.interface,
    )
    kwargs = {'session': instance.session,
              'endpoint_override': endpoint}

    client = panko_client(**kwargs)

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-event-api-version',
        metavar='<event-api-version>',
        default=utils.env(
            'OS_EVENT_API_VERSION',
            default=DEFAULT_EVENT_API_VERSION),
        help=(_('Event API version, default=%s '
                '(Env: OS_EVENT_API_VERSION)') %
              DEFAULT_EVENT_API_VERSION)
    )
    return parser
