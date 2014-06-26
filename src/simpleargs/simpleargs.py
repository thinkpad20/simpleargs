''' Simple argument parser for python '''
import json
import sys


class SimpleArgs(object):
    def __init__(self, raw_args, strict=False):
        try:
            self._called_with = raw_args[0]
        except IndexError:
            self._called_with = ''
        self._raw_args = raw_args
        self._options = {}
        self._args = []
        self._type_map = {}
        self._default_map = {}
        self._strict = strict
        self._aliases = {}
        self._no_auto_parse = False
        self._requireds = set()

        self._parse()

    # PUBLIC METHODS
    def add_alias(self, name1, name2):
        ''' Makes two flags equivalent, e.g. -f and --foo.'''
        if name1 in self._aliases:
            if self._aliases == name2:
                return
            else:
                raise ValueError("%s has already been assigned alias %s" %
                                 (name1, self._aliases[name1]))
        # See if this is an *actual* attribute on SimpleArgs.
        try:
            __getattribute__(self, name1)
            raise ValueError('%s cannot be used as an alias.' % name1)
        except:
            self._aliases[name1] = name2
            self._parse()

    def add_switch(self, *switches):
        '''Sets an argument name to be a boolean switch.'''
        for switch in switches:
            self._set_type(switch, bool)
        self._parse()

    def add_list(self, *names):
        '''Sets an argument name to be a list.'''
        for name in names:
            self._set_type(name, list)
        self._parse()

    def add_typed_list(self, name, _type):
        '''Sets an argument name to be a list of the given type.'''
        self._set_type(name, (list, _type))
        self._parse()

    def set_default(self, attr, default):
        '''Sets an argument name to map to a default value.'''
        self._default_map[attr] = default
        self._parse()

    def set_type(self, attr, _type):
        '''Sets the expected type of an argument name.'''
        self._set_type(attr, _type)
        self._parse()

    def toggle_auto_parse(self):
        '''Toggles the automatic parsing of numbers and booleans.'''
        self._no_auto_parse = not self._no_auto_parse
        self._parse()

    def add_requirement(self, name):
        '''Sets an argument to be required.'''
        self._requireds.add(name)
        self._parse()

    # PRIVATE METHODS

    def _set_type(self, attr, _type):
        assert isinstance(attr, basestring), "Name must be a string"
        if (self._strict and attr in self._type_map and
                self._type_map[attr] != _type):
            raise AssertionError("%s has already been assigned type %s" %
                                 (attr, self._type_map[attr]))
        self._type_map[attr] = _type

    def _resolve(self, alias, seen_aliases=None):
        '''Recursively resolves an alias. Converts hyphens to underscores.'''
        if seen_aliases is None:
            seen_aliases = set()
        result = self._aliases.get(alias)
        if result is None:
            return alias.replace('-', '_')
        if result in seen_aliases:
            raise ValueError("Cycle detected in aliases: %s" % seen_aliases)
        seen_aliases.add(alias)
        return self._resolve(result)

    def _get_option(self, flag):
        '''
        Reads an option and depending on how it's written, returns
        either a string or a tuple representing an option flag or a
        a=b setting.
        '''

        def make_option(option):
            splt = option.split("=")
            if len(splt) == 2 and len(splt[0]) > 0:
                return ("set", splt[0], splt[1])
            elif len(splt) == 1:
                return ("single", option)
            else:
                raise ValueError("Bad parse on option `%s`" % option)

        if flag.startswith("--") and len(flag) > 2:
            return make_option(flag[2:])
        elif flag.startswith("-") and len(flag) > 1:
            return make_option(flag[1:])
        else:
            return flag

    def _reset(self):
        ''' Resets the containers '''
        self._args = []
        self._options = {}

    def _parse(self):
        ''' Parses the argument vector. '''
        self._reset()
        # is either none if we're not reading an option, or some string
        active_opt = None
        for flag in self._raw_args[1:]:
            # get options
            option = self._get_option(flag)
            if isinstance(option, tuple):
                if active_opt is not None:
                    # if it's a list type, then we're done reading the list
                    if not self._is_list(active_opt):
                        # otherwise, we assume it's a bool type
                        self._set(active_opt, True)
                # this is the case of --foo=bar
                if option[0] == "set":
                    # set foo = bar
                    self._set(option[1], self._parse_setting(option[1], option[2]))
                    # we're not reading an option any more
                    active_opt = None
                # this is the case of --foo
                elif option[0] == "single":
                    # if option is a switch, then we can just set it here
                    if self._is_type(option[1], bool):
                        self._set(option[1], True)
                        active_opt = None
                    else:
                        # now we're reading a new option, 'foo'
                        active_opt = option[1]

            else:
                # if we're reading an option, like --foo bar, set it here
                if active_opt is not None:
                    option = self._parse_setting(active_opt, option)
                    if self._is_list(active_opt):
                        if active_opt in self._options:
                            self._extend(active_opt, option)
                        else:
                            self._set(active_opt, option)
                    else:
                        self._set(active_opt, option)
                        active_opt = None
                # if we're not reading an option, this is just an argument
                else:
                    self._args.append(option)

        # deal with the last option here
        if active_opt is not None:
            if not self._is_list(active_opt):
                self._set(active_opt, True)

        missing = [r for r in self._requireds if r not in self._options]
        if len(missing) > 0:
            raise LookupError("Required options %s were missing" % missing)

    def _set(self, attr, setting):
        '''Associates an attribute with a setting.'''
        attr = self._resolve(attr)
        self._options[attr] = setting

    def _extend(self, attr, setting_list):
        ''' used when appending to lists of attributes '''
        attr = self._resolve(attr)
        self._options[attr] += setting_list

    def _type_of(self, attr):
        ''' Gets the type of an attribute name '''
        return self._type_map.get(self._resolve(attr))

    def _is_type(self, attr, _type):
        ''' Convenience function to check type equation '''
        return self._type_of(attr) == _type

    def _is_list(self, attr):
        _type = self._type_of(attr)
        return _type == list or isinstance(_type, tuple) and _type[0] == list

    def _parse_setting_with_type(self, setting, _type, name=None):
        ''' Specialized behavior when we have specified a setting's type '''
        try:
            if _type == bool:
                if setting.lower() == "true":
                    return True
                else:
                    return False
                return self.parse_bool(setting)
            elif _type == list:
                return [self._auto_parse(setting)]
            elif isinstance(_type, tuple) and _type[0] == list:
                return [self._parse_setting_with_type(setting, _type[1])]
            elif _type == 'json':
                return json.loads(setting)
            else:
                return _type(setting)
        except ValueError:
            _nm = "(for option %s) " % name if name is not None else ""
            raise Exception("Failed to parse %s %s as %s" %
                            (setting, _nm, _type))

    def _auto_parse(self, setting):
        '''
        For numbers and bools, sees if they match and if so, converts them
        automagically.
        '''
        if self._no_auto_parse:
            return setting

        if setting.lower() == "true":
            return True

        if setting.lower() == "false":
            return False

        try:
            return int(setting)
        except ValueError:
            try:
                return float(setting)
            except ValueError:
                return setting

    def _parse_setting(self, name, setting):
        '''
        Converts settings into python objects. Could be as simple as strings,
        or a more complex parse.
        '''
        if name in self._type_map:
            return self._parse_setting_with_type(setting, self._type_map[name])
        else:
            return self._auto_parse(setting)

    def _get(self, attr, arg_type=None, default=None):
        if arg_type == bool:
            return self._options.get(attr, False)
        elif arg_type == str:
            return self._options.get(attr, "")
        elif arg_type == list:
            return self._options.get(attr, [])
        elif arg_type == int:
            return self._options.get(attr, 0)
        else:
            result = self._options.get(attr, default)
            if self._strict and attr not in self._default_map and result is None:
                raise AttributeError(attr)
            return result

    def _default(self, attr):
        return self._default_map.get(self._resolve(attr))

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except:
            return self._get(self._resolve(attr),
                             arg_type=self._type_of(attr),
                             default=self._default(attr))

    def __getitem__(self, item):
        if isinstance(item, basestring):
            return self.__getattr__(item)
        elif isinstance(item, int):
            if item < len(self._args):
                return self._args[item]
            else:
                return None

    def __iter__(self):
        return self._args.__iter__()

    def __len__(self):
        return len(self._args)

    def __str__(self):
        return ("SimpleArgs(Called with: %s, Arguments: %s, Options: %s)" %
                (self._called_with, self._args, self._options))


argv = SimpleArgs(sys.argv)
