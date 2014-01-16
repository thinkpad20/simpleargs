''' Simple argument parser for python '''
import sys

class SimpleArgs(object):
    def __init__(self, switches=None):
        self._name = sys.argv[0]
        self._options = {}
        self._args = []
        self.type_map = {}
        self.default_map = {}

        self.switches = switches or []
        for switch in self.switches:
            self.type_map[switch] = bool

        self.parse_args()

    def add_switch(self, switch):
        assert isinstance(switch, basestring), "Switch must be a string"
        self.switches.append(switch)
        self.parse_args()

    def set_default(self, attr, default):
        self.default_map[attr] = default

    def get_option(self, flag):
        '''
        Reads an option and depending on how it's written, returns
        either a string or a tuple representing an option flag or a
        a=b setting.
        '''

        def make_option(option):
            splt = option.split("=")
            if len(splt) == 2 and len(splt[0]) > 0:
                return ("set", splt[0], self.parse_setting(splt[1]))
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

    def reset(self):
        ''' resets the containers '''
        self._args = []
        self._options = {}

    def parse_args(self):
        ''' Parses the argument vector. '''
        self.reset()
        # is either none if we're not reading an option, or some string
        read_option = None
        for flag in sys.argv[1:]:
            # get options
            option = self.get_option(flag)
            if isinstance(option, tuple):
                # if we are trying to read an option now, it must be true/false
                if read_option is not None:
                    # just set it to True
                    self._options[read_option] = True
                # this is the case of --foo=bar
                if option[0] == "set":
                    # set foo = bar
                    self._options[option[1]] = self.parse_setting(option[2])
                    # we're not reading an option any more
                    read_option = None
                # this is the case of --foo
                elif option[0] == "single":
                    # if option is a switch, then we can just set it here
                    if option[1] in self.switches:
                        self._options[option[1]] = True
                        read_option = None
                    else:
                        # now we're reading a new option, 'foo'
                        read_option = option[1]

            elif isinstance(option, basestring):
                # if we're reading an option, like --foo bar, set it here
                if read_option is not None:
                    self._options[read_option] = self.parse_setting(option)
                    read_option = None
                # if we're not reading an option, this is just an argument
                else:
                    self._args.append(option)

        # deal with the last option here
        if read_option is not None:
            self._options[read_option] = True

    def parse_setting(self, setting):
        '''
        Just a wrapper that converts True/False into their python equivalents
        '''
        if setting in self.type_map:
            if self.type_map[setting] == bool:
                # bool parsing is weird in python so we just do it here
                if setting.lower() == "true":
                    return True
                elif setting.lower() == "false":
                    return False
            else:
                return self.type_map[setting](setting)
        # could parse numbers here?
        else:
            return setting

    def get(self, attr, arg_type=None, default=None):
        if arg_type == bool:
            return self._options.get(attr, False)
        elif arg_type == str:
            return self._options.get(attr, "")
        else:
            return self._options.get(attr, default)

    def __getattr__(self, attr):
        return self.get(attr,
                        arg_type=self.type_map.get(attr),
                        default=self.default_map.get(attr))

    def __getitem__(self, item):
        if isinstance(item, basestring):
            return self.__getattr__(item)
        elif isinstance(item, int):
            if item < len(self._args):
                return self._args[item]
            else:
                return None

argv = SimpleArgs()
