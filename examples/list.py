from simpleargs import argv

argv.add_list("names")
argv.add_list("ages") # we can also specify multiple attributes in `add_list`

names_ages = sorted(zip(argv.names, argv.ages), key=lambda x: x[1])

for name, age in names_ages:
    print "%s is %s years old" % (name, age)

print "%s is the oldest!" % names_ages[-1][0]
