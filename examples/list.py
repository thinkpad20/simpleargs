from simpleargs import argv

argv.add_list("names", "ages")
argv.add_switch("switch")
argv.add_alias("s", "switch")

print argv.names
print argv.ages

assert len(argv.names) == len(argv.ages), "Different number of names and ages"

names_ages = zip(argv.names, argv.ages)

for name, age in names_ages:
    print "%s is %s years old" % (name, age)

sorted_n_a = sorted(names_ages, key=lambda tup: tup[1])

print "%s is the youngest at %s years old" % (sorted_n_a[0][0],
                                              sorted_n_a[0][1])


if argv.switch:
    print "Looks like you flipped the switch"
else:
    print "switch was not flipped!"

for arg in argv:
    print arg
