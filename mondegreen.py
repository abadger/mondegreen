#!/usr/bin/python3 -tt
#
# Author: Toshio Kuratomi <toshio@fedoraproject.org>
# Copyright: November, 2014
# License: GPLv3+
#

import sys
import asyncio

from mondegreen.idonethis import IDoneThis


class Poster(IDoneThis):
    @asyncio.coroutine
    def async_post(self, msg):
        self.post(msg, self.information)

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

