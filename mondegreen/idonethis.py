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
---------------------
idonethis.com adapter
---------------------

An adapter to talk to idonethis.

.. seealso::

    `idonethis API documentation <https://idonethis.com/api/>`

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''

import asyncio

import aiohttp

IDONETHISENDPOINT = 'https://idonethis.com/api/v0.1/dones/'

class IDoneThisPostingError(Exception):
    pass

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

    @asyncio.coroutine
    def post(self, msg, team=None):
        team = team if team else self.default_team

        headers = self.auth_header
        data = dict(team=team, raw_text=msg)
        reply = yield from aiohttp.request('post', self.base_url,
                headers=headers, data=data)

        if reply.status < 200 or reply.status > 300:
            try:
                data = yield from reply.json()
            except Exception as e:
                raise e # Temporary - figure out what could happen here
                response_msg = reply.text

            if 'errors' in data:
                response_msg = repr(data['errors'])
            elif 'warnings' in data:
                response_msg = repr(data['warnings'])
            else:
                response_msg = data['text']

            raise IDoneThisPostingError('IDoneThis server code: {0},'
                ' reply:{1}'.format(reply.status, response_msg))

        return data


