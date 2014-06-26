import unittest

from simpleargs import SimpleArgs


class SimpleArgsTest(unittest.TestCase):
    '''Tests the expected behavior of SimpleArgs'''

    def make(self, *input_args):
        # import pdb; pdb.set_trace()
        return SimpleArgs(['python test.py'] + list(input_args))

    def test_empty(self):
        '''Tests the behavior when no args are given.'''
        argv = self.make()
        self.assertEqual(argv._called_with, 'python test.py')
        self.assertEqual(len(argv), 0)

    def test_plain_args(self):
        '''Tests when we don't have any flags.'''
        argv = self.make('foo', 'bar', 'baz')
        self.assertEqual(len(argv), 3)
        self.assertEqual(argv[0], 'foo')
        self.assertEqual(argv[1], 'bar')
        self.assertEqual(argv[2], 'baz')

    def test_boolean_flags(self):
        '''Tests that flags without values are boolean.'''
        argv = self.make('foo', 'bar', '--baz')
        self.assertEqual(len(argv), 2)
        self.assertTrue(argv.baz)

    def test_keyvals(self):
        '''Tests setting key/value pairs.'''
        # Test with singles.
        argv = self.make('--foo', 'bar')
        self.assertEqual(argv.foo, 'bar')

        # Test with multiples.
        argv = self.make('--foo', 'bar', '--baz', 'qux', '--fizz', 'buzz')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv.baz, 'qux')
        self.assertEqual(argv.fizz, 'buzz')

        # Test with multiples, some with double dashes and some with single.
        argv = self.make('--foo', 'bar', '-baz', 'qux', '-fizz', 'buzz')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv.baz, 'qux')
        self.assertEqual(argv.fizz, 'buzz')

        # Test with both flags and keyvals.
        argv = self.make('-foo', 'bar', 'baz', 'qux')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv[0], 'baz')
        self.assertEqual(argv[1], 'qux')

        # Test with both flags and keyvals, flags at the end.
        argv = self.make('baz', 'qux', '-foo', 'bar')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv[0], 'baz')
        self.assertEqual(argv[1], 'qux')

        # Test with both flags and keyvals, flags at beginning and end.
        argv = self.make('-a', 'b', 'baz', 'qux', '-foo', 'bar', 'buzz')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv.a, 'b')
        self.assertEqual(argv[0], 'baz')
        self.assertEqual(argv[1], 'qux')
        self.assertEqual(argv[2], 'buzz')

        # Tests that we can use `=` if we choose.
        argv = self.make('-a=b', 'baz', 'qux', '-foo=bar')
        self.assertEqual(argv.foo, 'bar')
        self.assertEqual(argv.a, 'b')
        self.assertEqual(argv[0], 'baz')
        self.assertEqual(argv[1], 'qux')

    def test_defaults(self):
        '''Tests that we can define defaults.'''
        argv = self.make()
        self.assertIs(argv.name, None)
        argv.set_default('name', 'Allen')
        self.assertEqual(argv.name, 'Allen')

        # Make sure the default can be overriden.
        argv = self.make('--bloop', 'bleep', 'hey', 'there')
        argv.set_default('bloop', 'fleep')
        self.assertEqual(argv.bloop, 'bleep')

    def test_convert_dashes(self):
        '''Tests that we convert dashes into underscores.'''
        argv = self.make('--with-dashes', 'hey')
        self.assertEqual(argv.with_dashes, 'hey')
        argv = self.make('foo', 'bar', '--some-flag')
        self.assertTrue(argv.some_flag)

    def test_parsing(self):
        '''Tests that we automatically parse numbers and bools.'''
        argv = self.make('--num', '3', '--bool', 'True')
        self.assertEqual(argv.num, 3)
        self.assertEqual(argv.bool, True)

        argv.toggle_auto_parse()
        self.assertEqual(argv.num, '3')
        self.assertEqual(argv.bool, 'True')

    def test_types(self):
        '''Tests that we can change the type of a flag.'''
        argv = self.make('--info', '{"foo": "bar"}')
        argv.set_type('info', 'json')
        self.assertEqual(argv.info, {'foo': 'bar'})

    def test_lists(self):
        '''Tests that we can make lists.'''
        argv = self.make('--nums', '4', '5', '6', '--strs', 'hello', 'world')
        argv.add_list('nums', 'strs')
        self.assertEqual(argv.nums, [4, 5, 6])
        self.assertEqual(argv.strs, ['hello', 'world'])

        argv.add_typed_list('nums', float)
        self.assertEqual(argv.nums, [4.0, 5.0, 6.0])

    def test_aliases(self):
        '''Tests that we can alias two different names.'''
        argv = self.make('-f', 'floop')
        argv.add_alias('f', 'floobadoobadoop')
        self.assertEqual(argv.f, 'floop')
        self.assertEqual(argv.floobadoobadoop, 'floop')

        # Now try it in the reverse direction
        argv = self.make('-floobadoobadoop', 'floop')
        argv.add_alias('f', 'floobadoobadoop')
        self.assertEqual(argv.f, 'floop')
        self.assertEqual(argv.floobadoobadoop, 'floop')

        # Now try it twice. The second one should stick.
        argv = self.make('-floobadoobadoop', 'floop', '-f', 'fleep')
        argv.add_alias('f', 'floobadoobadoop')
        self.assertEqual(argv.f, 'fleep')
        self.assertEqual(argv.floobadoobadoop, 'fleep')


if __name__ == '__main__':
    unittest.main()
