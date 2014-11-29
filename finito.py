#!/usr/bin/python3 -tt

import os
import sys
#import asyncio
import argparse

from configobj import ConfigObj

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
        raise ValidateError('invalid filter types specified: %s'.format(
            keys.difference(IDONETHIS_FILTERS)))

    return value

validator = Validator({'idt_read_filter':'idt_read_filter_check'})
configspec = '''
[idonethis]
auth_token=string
posting_team=string
read_filter=idonethis_read_filter

[slack]
webhook=url
posting_channel=string
'''.splitlines()

#class Poster(IDoneThis):
#    @asyncio.coroutine
#    def async_post(self, msg):
#        self.post(msg, self.information)

#class Terminal:
#    @asyncio.coroutine
#    def read_input(self):
#        yield from raw_input

def parse_args(args=None):

    parser = argparse.ArgumentParser(description='Post to idonethis')
    parser.add_argument('--config-file', '-f', dest='config', action='append',
            default=list())
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--idonethis-posting-team',
            dest='idonethis_posting_team')
    parser.add_argument('--slack-posting-channel',
            dest='slack_posting_channel')
    parser.add_argument('message', nargs='+')

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    args.message = ' '.join(args.message)
    return args

def read_config(config_files):
    if isinstance(config_files, str):
        config_files = (config_files,)
    cfg = ConfigObj(configspec=configspec)
    for cfg_file in config_files:
        cfg_from_file = ConfigObj(cfg_file, configspec=configspec)
        cfg_from_file.validate(validator)
        cfg.merge(cfg_from_file)
    return cfg

def cli_to_config(args):
    cfg = ConfigObj(configspec=configspec)

    cfg['idonethis'] = {}
    if args.idonethis_posting_team:
        cfg['idonethis']['posting_team'] = args.idonethis_posting_team

    cfg['slack'] = {}
    if args.slack_posting_channel:
        cfg['slack']['posting_channel'] = args.slack_posting_channel

    cfg.validate(validator)
    return cfg

def main(args):
    args = parse_args()

    config = ConfigObj(configspec=configspec)
    for default_cfg_file in ('/etc/mondegreen.ini',
            os.path.expanduser('~/.mondegreen.ini')):
        try:
            cfg = read_config(default_cfg_file)
            config.merge(cfg)
        except OSError:
            # Okay if default files don't exist
            pass
    if args.config:
        cfg = read_config(args.config)
        config.merge(cfg)

    config.merge(cli_to_config(args))

    idt = IDoneThis(config['idonethis']['auth_token'],
            config['idonethis']['posting_team'])
    idt.post(args.message)
    sys.exit(0)

    # get message from user
    # when message received, post message to idt
    # wait for new message from user

if __name__ == '__main__':
    main(sys.argv)
