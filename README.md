# SimpleArgs
## An easy way to parse arguments in python

### Motivation

Parsing command-line arguments is a frequent task. Python has a powerful argument parser library, but it's often overkill and requires reading a lot of docs and somewhat tedious configuration. This aims to make a simple way to do the same thing, in as intuitive a manner possible.

### Examples

Let's see it in action!

```python
from simpleargs import argv

print "Here are your arguments:"
for arg in argv:
    print arg
```

Run this with:

```
> python arg1.py hello world hey
Here are your arguments:
hello
world
hey
```

Simple enough, right? That's nothing new though. How about some flags?

```python
from simpleargs import argv

if argv.choice == "correct":
    print "You have chosen wisely"
elif argv.benice:
    print "OK, I'll let it slide"
else:
    print "Oh noes!"
```

Trying it out:

```
> python choice.py --choice correct
You have chosen wisely
> python choice.py --choice=correct
You have chosen wisely
> python choice.py --benice -choice=incorrect
OK, I'll let it slide
> python choice.py
Oh noes!
```

So you can see that single `--flag`s are treated as bools by default. Also, you can see that specifying an option with `=`, or with simple juxtaposition, are both supported, as are single or double hyphens.

Let's look at some defaults!

```python
from simpleargs import argv

argv.add_default("name", "Allen")

print "Hello, %s! How are you?" % argv.name
```

Testing it:

```
> python defaults.py
Hello, Allen! How are you?
> python defaults.py --name Scott
Hello, Scott! How are you?
```

What about numbers?

```python
from simpleargs import argv

argv.set_type("age", int)

if argv.age >= 21:
    print "Have a beer!"
else:
    print "Wait %s more years!" % (21 - age)
```

Test it with:

```
> python beerme.py --age 25
Have a beer!
> python beerme.py --age=19
Wait 2 more years!
```

Play around with it!
