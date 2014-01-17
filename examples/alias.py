from simpleargs import argv

argv.add_alias("o", "this_is_a_long_option")

if argv.o:
    print "Option was true!"
else:
    print "Option was false!"

if argv.this_is_a_long_option:
    print "Option was true!"
else:
    print "Option was false!"
