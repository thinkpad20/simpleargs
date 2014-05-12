# SimpleArgs
### the python argument parser you already know how to use!

### Motivation

Parsing command-line arguments is a frequent task. Python has a powerful argument parser library, and there are other alternatives like docopt. But these all require reading a lot of docs and learning new APIs. They're often overkill for quick-and-dirty scripts where you just need to grab a few key pieces of information. SimpleArgs aims to let you access your arguments in as simple and intuitive a manner possible. You can get 90% of the way there just by writing:

```python
from simpleargs import argv
```

Most arguments are parsed without any configuration at all, simply ending up as boolean flags or key/value pairs as appropriate. Numbers and booleans are parsed automatically. Some more advanced features like lists, aliases, required arguments, etc are also easily available.

### Installing and using

SimpleArgs is on pypi, so give it a try with `pip install simpleargs`. It's tiny (~36kb) and has no external dependencies.

### Examples

Let's see it in action!

#### Echo program

```python
from simpleargs import argv
print ' '.join(argv)
```

Running it:

```
> python echo.py hello world!
hello world!
```

#### Simple flask server:

```python
from flask import Flask
from simpleargs import argv

app = Flask(argv.name or __name__)
app.route('/<name>/')(lambda name: 'Hello, %s' % name)
app.run(port=argv.port or 7890, use_reloader=argv.use_reloader)
```

Running it:

```
> python flask_ex.py --port 8080
 * Running on http://127.0.0.1:8080/
```

#### General arguments (not key-value pairs)

```python
from simpleargs import argv

print 'Here are your arguments:'
for arg in argv:
    print arg
```

Run this with:

```
> python simple.py hello world hey
Here are your arguments:
hello
world
hey
> python simple.py -option setting these are args
Here are your arguments:
these
are
args
```

The first is self-explanatory and equivalent to just using `sys.argv`. In the second example, the argument `setting` is consumed as the value of `option` (see below) and the rest are treated as general arguments.

#### Simple key/value pairs

```python
from simpleargs import argv

if argv.choice == 'correct':
    print 'You have chosen wisely'
elif argv.be_nice:
    print "OK, I'll let it slide"
else:
    print 'Oh noes!'
```

Trying it out:

```
> python choice.py --choice correct
You have chosen wisely
> python choice.py --choice=correct
You have chosen wisely
> python choice.py --be_nice -choice=incorrect
OK, I'll let it slide
> python choice.py
Oh noes!
```

So you can see that single `--flag`s are treated as bools by default. Also, you can see that specifying an option with `=`, or with simple juxtaposition, are both supported, as are single or double hyphens.

#### Specifying defaults

```python
from simpleargs import argv

argv.set_default('name', 'Allen')

print 'Hello, %s! How are you?' % argv.name
```

Testing it:

```
> python default.py
Hello, Allen! How are you?
> python default.py --name Scott
Hello, Scott! How are you?
```

#### Numbers

```python
from simpleargs import argv

if argv.age >= 21:
    print 'Have a beer!'
else:
    print 'Wait %s more years!' % (21 - argv.age)
```

Test it with:

```
> python beer.py --age 25
Have a beer!
> python beer.py --age=19
Wait 2 more years!
```

Ints, floats and bools are automatically parsed as such, if possible. If this behavior is undesirable, either turn off autoparsing with `argv.no_auto_parse()`, or set the type manually (for example, with `argv.set_type('zipcode', str)`), which will override the autoparsing.

#### Lists

We can have keys map to lists if we declare them as such:

```python
from simpleargs import argv

argv.add_list('names')
argv.add_list('ages') # we can also specify multiple attributes in `add_list`

names_ages = sorted(zip(argv.names, argv.ages), key=lambda x: x[1])

for name, age in names_ages:
    print '%s is %s years old' % (name, age)

print '%s is the oldest!' % names_ages[-1][0]
```

Test:

```
> python list.py --names Allen Scott Caroline --ages 28 26 30
Scott is 26 years old
Allen is 28 years old
Caroline is 30 years old
Caroline is the oldest!
```

#### Aliases

Sometimes we want to make a verbose option easy to read but easy to write when we already know what it means.

```python
from simpleargs import argv

argv.add_alias('o', 'this_is_a_long_option')

if argv.o:
    print 'Short option was true!'
else:
    print 'Short option was false!'

if argv.this_is_a_long_option:
    print 'Long option was true!'
else:
    print 'Long option was false!'
```

Test:

```
> python alias.py -o true
Short option was true!
Long option was true!
> python alias.py --this_is_a_long_option false
Short option was false!
Long option was false!
```

### Contributing

This is very new and very experimental, so play around with it. Feel free to submit all kinds of pull requests!
