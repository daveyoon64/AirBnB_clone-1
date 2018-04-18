#!/usr/bin/python3
"""starts the Flask server"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """list all State objects present in DBStorage"""
    states = storage.all('State').values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def remove_session(exception=None):
    """remove current SQL Alcehmy session"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
