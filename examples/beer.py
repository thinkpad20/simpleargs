from simpleargs import argv

argv.set_type("age", int)

if argv.age >= 21:
    print "Have a beer!"
else:
    print "Wait %s more years!" % (21 - argv.age)
