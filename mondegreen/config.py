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
--------------------------------
Base Config and Argument Parsing
--------------------------------

In Mondegreen, configuration and argument parsing are somewhat merged.  Most
arguments are saved into a :class:`~configobj.ConfigObj` and accessed from
there.

This module sets up pieces of the configuration that any program using the
mondegreen framework will have access to.  Configuration of the adapters, for
instance.  Everything in here should be extendable by the individual
Mondegreen program.  That way, the different services can add additional
config values and command line switches.

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''

import ast
from argparse import ArgumentParser
from urllib.parse import urlparse

from validate import Validator, ValidateError

from . import __version__

### TODO: The validators and configspec specific to an adaptor should be
### placed alongside the adaptor rather than here.  Need a plugin system
### that we can iterate over to load them into the default set.

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

class BaseArgParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(BaseArgParser, self).__init__(*args, **kwargs)
        self.add_argument('--config-file', '-f', dest='config', action='append',
                default=list())
        self.add_argument('--version', action='version', version=__version__)
        self.add_argument('--idt-posting-team',
                dest='idt_posting_team')
        self.add_argument('--slack-posting-channel',
                dest='slack_posting_channel')

