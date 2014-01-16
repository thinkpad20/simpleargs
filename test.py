from simpleargs import argv

argv.add_switch("baz")
argv.set_default("blorp", 55)

print "simpleargs.foo: %s" % argv.foo
print "simpleargs.bar: %s" % argv.bar
print "simpleargs.baz: %s" % argv.baz
print "simpleargs.blorp: %s" % argv.blorp
print "simpleargs args: %s" % argv._args

print "bloop: %s" % argv["bloop"]
print "2nd arg: %s" % argv[1]
