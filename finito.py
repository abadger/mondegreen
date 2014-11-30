#!/usr/bin/python3 -tt
#
# Author: Toshio Kuratomi <toshio@fedoraproject.org>
# Copyright: November, 2014
# License: GPLv3+
#

import os
import sys
#import asyncio
import argparse

from configobj import ConfigObj

from mondegreen.conman import ConfigManager
from mondegreen.idonethis import IDoneThis

__version__ = '0.1'

import ast
from validate import Validator, ValidateError

IDONETHIS_FILTERS = frozenset(('team',))

def idt_read_filter_check(value):
    value = ast.literal_eval(value)
    if not isinstance(value, dict):
        raise ValidateError('read_filter must be a dict')

    keys = frozenset(value.keys())
    if not keys.issubset(IDONETHIS_FILTERS):
        raise ValidateError('invalid filter types specified: {0}'.format(
            keys.difference(IDONETHIS_FILTERS)))

    return value

from urllib.parse import urlparse
def url_filter_check(value, schemes=('http', 'https'), non_local=True):
    expanded = urlparse(value)

    if expanded.scheme not in schemes:
        raise ValidateError('url not one of the allowed schemes: {0}'.format(
            schemes))

    if non_local and not expanded.netloc:
        raise ValidateError('url must specify a remote server')

    return value

validator = Validator({'idt_read_filter': idt_read_filter_check,
    'url': url_filter_check})

combinedspec = '''
[idonethis]
auth_token=string
posting_team=string|idt_posting_team
read_filter=idt_read_filter

[slack]
webhook=url
posting_channel=string|slack_posting_channel
'''.splitlines()

#class Poster(IDoneThis):
#    @asyncio.coroutine
#    def async_post(self, msg):
#        self.post(msg, self.information)

#class Terminal:
#    @asyncio.coroutine
#    def read_input(self):
#        yield from raw_input

def arg_parser():

    parser = argparse.ArgumentParser(description='Post to idonethis')
    parser.add_argument('--config-file', '-f', dest='config', action='append',
            default=list())
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--idonethis-posting-team',
            dest='idonethis_posting_team')
    parser.add_argument('--slack-posting-channel',
            dest='slack_posting_channel')
    parser.add_argument('message', nargs='+')

    return parser


def main(args):
    confmgr = ConfigManager(combinedspec, validator, arg_parser())

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
    idt.post(args.message)

    sys.exit(0)

    # get message from user
    # when message received, post message to idt
    # wait for new message from user

if __name__ == '__main__':
    main(sys.argv)
