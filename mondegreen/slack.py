# Author: Toshio Kuratomi <toshio@fedoraproject.org>
# Copyright: November, 2014
# License: LGPLv3+
#

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
