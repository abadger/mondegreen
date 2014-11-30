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
------
Finito
------

Finito is a command line application for posting short messages to a web
service.  It'd currently being used with idonethis but could be adapted to
publish to other twitter-like services in the future.

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''

import os
import sys
import asyncio
import argparse

from mondegreen.conman import ConfigManager
from mondegreen.config import BaseArgParser, combinedspec, validator
from mondegreen.idonethis import IDoneThis

def main(args):
    arg_parser = BaseArgParser(description='Post to idonethis')
    arg_parser.add_argument('message', nargs='+')
    confmgr = ConfigManager(combinedspec, validator, arg_parser)

    for default_cfg_file in ('/etc/mondegreen.ini',
            os.path.expanduser('~/.mondegreen.ini')):
        try:
            confmgr.add_config(default_cfg_file)
        except OSError:
            # Okay if default files don't exist
            pass

    args = confmgr.add_args()
    args.message = ' '.join(args.message)
    config = confmgr.cfg

    idt = IDoneThis(config['idonethis']['auth_token'],
            config['idonethis']['posting_team'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(idt.post(args.message))

    sys.exit(0)

    # get message from user
    # when message received, post message to idt
    # wait for new message from user

if __name__ == '__main__':
    main(sys.argv)
