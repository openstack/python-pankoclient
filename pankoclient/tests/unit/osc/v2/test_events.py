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

from pankoclient.osc.v2 import events
from pankoclient.tests.unit import base as test_base
from pankoclient.v2 import events as events_mgr


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
