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
from six.moves.urllib import parse as urllib_parse


def get_pagination_options(limit=None, marker=None, sorts=None):
    options = []
    if limit:
        options.append("limit=%d" % limit)
    if marker:
        options.append("marker=%s" % urllib_parse.quote(marker))
    for sort in sorts or []:
        options.append("sort=%s" % urllib_parse.quote(sort))
    return "&".join(options)


def filtersdict_to_url(filters):
    urls = []
    for k, v in sorted(filters.items()):
        url = "q.field=%s&q.op=eq&q.value=%s" % (k, v)
        urls.append(url)
    return '&'.join(urls)
