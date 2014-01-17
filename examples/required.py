from simpleargs import argv

argv.add_requirement("foo")

print "Foo = %s" % argv.foo
