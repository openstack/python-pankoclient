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

import mock

from pankoclient.tests.unit import base as test_base
from pankoclient.v2 import events as events_mgr
from pankoclient.v2 import events_cli as events


@mock.patch.object(events_mgr.EventTypeManager, '_list')
class TestEventTypeList(test_base.TestEventV2):
    def setUp(self):
        super(TestEventTypeList, self).setUp()
        self.cmd = events.EventTypeList(self.app, None)

    def test_event_type_list(self, mock_list):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        mock_list.assert_called_once_with('/v2/event_types/')


@mock.patch.object(events_mgr.EventTraitsManager, '_list')
class TestEventTraitsList(test_base.TestEventV2):
    def setUp(self):
        super(TestEventTraitsList, self).setUp()
        self.cmd = events.EventTraitList(self.app, None)

    def test_event_traits_list(self, mock_list):
        arglist = [
            'event_type1',
            'trait_name1'
        ]
        verifylist = [
            ('type_name', 'event_type1'),
            ('trait_name', 'trait_name1'),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        expected_url = '/v2/event_types/%s/traits/%s' % (
            parsed_args.type_name, parsed_args.trait_name)
        mock_list.assert_called_once_with(expected_url)


@mock.patch.object(events_mgr.EventTraitDescriptionManager, '_list')
class TestEventTraitDescription(test_base.TestEventV2):
    def setUp(self):
        super(TestEventTraitDescription, self).setUp()
        self.cmd = events.EventTraitDescription(self.app, None)

    def test_event_type_traits_description(self, mock_list):
        arglist = [
            'event_type1',
        ]
        verifylist = [
            ('type_name', 'event_type1'),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        expected_url = '/v2/event_types/%s/traits/' % parsed_args.type_name
        mock_list.assert_called_once_with(expected_url)
