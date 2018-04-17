#!/usr/bin/python3
"""Starts Flask web application with route that check int"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    new = text.replace('_', ' ')
    return 'C {}'.format(new)


@app.route('/python')
@app.route('/python/<text>')
def python_text(text=None):
    if not text:
        text = 'is_cool'
    new = text.replace('_', ' ')
    return 'Python {}'.format(new)


@app.route('/number/<int:n>')
def number(n):
    return '{} is a number'.format(n)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
