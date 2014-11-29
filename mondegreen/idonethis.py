# Author: Toshio Kuratomi <toshio@fedoraproject.org>
# Copyright: November, 2014
# License: LGPLv3+
#

import requests

IDONETHISENDPOINT = 'https://idonethis.com/api/v0.1/dones/'

class IDoneThis:
    def __init__(self, auth_token, default_team=None, filters=None):
        self.base_url = IDONETHISENDPOINT
        self.auth_token = auth_token
        self.filters = filters or []
        self.default_team = default_team

    @property
    def auth_header(self):
        return dict(Authorization='Token {0}'.format(self.auth_token))

    def sync(self, maximum=1000):
        # From newest to oldest, read in the dones and enter them into a db
        return data

    def latest(self):
        self.sync()
        headers = dict(Authorization='Token {0}'.format(self.auth_token))
        reply = requests.get()
        return data

    def history(self, refresh=False):
        return data

    def search(self, refresh=False):
        return data

    def post(self, msg, team=None):
        team = team if team else self.default_team

        headers = self.auth_header
        data = dict(team=team, raw_text=msg)
        reply = requests.post(self.base_url, headers=headers, data=data)

        if reply.status_code < 200 or reply.status_code > 300:
            try:
                data = reply.json()
            except Exception as e:
                raise e # Temporary - figure out what could happen here
                response_msg = data['text']

            if 'errors' in data:
                response_msg = repr(data['errors'])
            elif 'warnings' in data:
                response_msg = repr(data['warnings'])
            else:
                response_msg = data['text']

            raise IDoneThisPostingError('IDoneThis server code: {0},'
                ' reply:{1}'.format(reply.status_code, response_msg))

        return data


