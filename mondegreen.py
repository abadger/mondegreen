#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Toshio Kuratomi
# License: GPLv3+
#
# This file is part of Mondegreen.
#
# Mondegreen is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This file is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this file.  If not, see <http://www.gnu.org/licenses/>.
#
'''
----------
Mondegreen
----------

Mondegreen is a server application that reads content from multiple sources
and republishes it on another one.  It can be used to create a single source
of information for users.

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''

import sys
import asyncio

from mondegreen.idonethis import IDoneThis


class Terminal:
    @asyncio.coroutine
    def read_input(self):
        yieldr from raw_input

def main(args):
    # Get configuration
    args = parse_args(args)
    config = read_config(args)
    config = merge(config, args)

    idt = Poster(config.auth_token, team)
    loop = asyncio.get_event_loop()
    # get message from user
    # when message received, post message to idt
    # wait for new message from user
    idt.post(msg)

if __name__ == '__main__':
    main(sys.argv)

def main(args):
    idonethis = IDoneThis()
    slack = Slack()

    # Sync IDoneThis with a limit into our db
    # Check whether there's any new postings compared to what we've sent out
    # Push any new postings to slack

