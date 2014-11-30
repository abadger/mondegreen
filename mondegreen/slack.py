# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Toshio Kuratomi
# License: GPLv3+
#
# This file is part of Mondegreen
#
# This file is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This file is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this file.  If not, see <http://www.gnu.org/licenses/>.
#
'''
-----------------
slack.com adapter
-----------------

An adapter to talk to slack

.. seealso::

    `slack API documentation <https://slack.com/api/>`

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''

import json
from urllib.parse import urlencode
import requests

class SlackPostingError(Exception):
    pass

class Slack:
    def __init__(self, auth_url, default_channel,
            agent_name='Arbitrary Bits'):
        self.auth_url = auth_url
        self.channel = default_channel
        self.agent_name = agent_name
        self.channel = default_channel


    def post(self, msg, icon=None, channel=None):
        channel = channel if channel else self.channel
        payload = dict(channel=channel, username=self.agent_name, text=msg)
        if icon:
            paylod['icon_emoji'] = icon

        data = dict(payload=json.dumps(payload))
        reply = requests.post(self.auth_url, data=data)
        if reply.text.strip() != 'ok':
            raise SlackPostingError('Slack server code: {0},'
                ' reply:{1}'.format( reply.status_code, reply.text))
