from simpleargs import argv

if argv.choice == "correct":
    print "You have chosen wisely"
elif argv.be_nice:
    print "OK, I'll let it slide"
else:
    print "Oh noes!"
