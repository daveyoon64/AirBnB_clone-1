#!/usr/bin/python3
"""Starts Flask web application with python route"""
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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
