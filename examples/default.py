from simpleargs import argv

argv.set_default("name", "Allen")

print "Hello, %s! How are you?" % argv.name
