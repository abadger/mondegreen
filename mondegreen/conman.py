# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Toshio Kuratomi
#
# Special License: LGPLv3+
#
# This file is part of Mondegreen but it carries a different license than the
# rest of the source code.  Most of Mondegreen is GPLv3 or later but this file
# is distributed under the terms of the LGPLv3+.  This was chosen for this
# file as the code and techniques here could be generally relevant to other
# programs and I wish that other programers can use them more freely than the
# terms of the GPL allow.
#
# This file is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This file is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Toshio Kuratomi <toshio@fedoraproject.org>

'''
------------------
Configuration code
------------------

Be it from a config file or command line switches, most every program needs to
take some configuration information.  More elaborate programs may want to take
configuration from multiple sources (defaults, system-wide and per-user config
files, the command line, and variables) and merge them into one.  With the
help of ConfigObj, we implement something to handle all of that here.

.. seealso::

    Mozilla's `configman
    <http://configman.readthedocs.org/en/latest/introduction.html>` does
    something similar to this but it is not yet python3 compatible

.. codeauthor:: Toshio Kuratomi <toshio@fedoraproject.org>
.. sectionauthor:: Toshio Kuratomi <toshio@fedoraproject.org>

.. versionadded:: 0.1
'''
from collections import defaultdict

from configobj import ConfigObj

def variable_level_defaultdict():
    return defaultdict(variable_level_defaultdict)

class ConfigManager:
    def __init__(self, combinedspec, validator, arg_parser):
        self.argspec = variable_level_defaultdict()
        if isinstance(combinedspec, str):
            combinedspec = combinedspec.splitlines()
        self._parse_spec(combinedspec)

        self.validator = validator
        self.arg_parser = arg_parser

        self.cfg = ConfigObj(configspec=self.configspec)

    def _make_argspec(self, section, key):
        combined = section[key].rsplit('|', 1)
        if len(combined) > 1 and combined[1]:
            child = section
            section[key] = combined[0]
            sections = [key]
            while child.parent is not child:
                sections.append(child.name)
                child = child.parent
            self.argspec[combined[1]] = sections[::-1]

    def _parse_spec(self, combinedspec):
        spec = ConfigObj(combinedspec)
        spec.walk(self._make_argspec)
        self.configspec = spec.write()

    def add_config(self, config_files):
        '''
        Read a list of config files and merge their settings into the config

        :arg config_files: sequence of config filenames or a single filename
        '''
        if isinstance(config_files, str):
            config_files = (config_files,)

        for cfg_file in config_files:
            cfg_from_file = ConfigObj(cfg_file, configspec=self.configspec)
            cfg_from_file.validate(self.validator)
            self.cfg.merge(cfg_from_file)

    def add_args(self, args=None, consume=True):
        '''
        Add a command line argument list to the config

        :kwarg args: list of command line args, like sys.argv.  If no
            arguments are given, then sys.argv is parsed.  Just like
            :meth:`argparse.ArgumentParser.parse` you should not pass sys.argv
            to this method unless you first remove the program's name from the
            argument list.
        :kwarg consume: With the default of True, command line arguments that
            are added to the config are removed from the arguments.  If False,
            those arguments are left in the args that are returned to the user.
        :returns: an `argparse.Namespace` object with the values parsed from
            the argument list.  This is just like what would be returned by
            calling the :meth:`~argparse.ArgumentParser.parse` method.
        '''
        args = self.arg_parser.parse_args(args)

        if args.config:
            self.add_config(args.config)

        cfg = ConfigObj(configspec=self.configspec)

        for arg_name in self.argspec:
            if hasattr(args, arg_name) and getattr(args, arg_name) is not None:
                parent = cfg
                section = cfg
                for section_name in self.argspec[arg_name]:
                    parent = section
                    try:
                        section = parent[section_name]
                    except KeyError:
                        parent[section_name] = dict()
                        section = parent[section_name]

                parent[section_name] = getattr(args, arg_name)
                if consume:
                    delattr(args, arg_name)

        self.cfg.merge(cfg)
        return args
