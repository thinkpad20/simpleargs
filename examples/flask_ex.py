'''Note: Requires Flask'''
from flask import Flask
from simpleargs import argv

app = Flask(argv.name or __name__)
app.route('/<name>/')(lambda name: 'Hello, %s' % name)
app.run(port=argv.port or 7890, use_reloader=argv.use_reloader)
