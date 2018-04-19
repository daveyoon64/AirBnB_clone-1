#!/usr/bin/python3
"""starts the Flask server"""
import sys
from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
@app.route('/states/')
def states_list():
    """list all State objects present in DBStorage"""
    states = storage.all('State').values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def states_id_list(id=None):
    """list all State objects present in DBStorage"""
    found_id = None
    name = None
    states = storage.all('State').values()
    cities = storage.all('City').values()
    for state in states:
        if state.id == id:
            found_id = state.id
            name = state.name
    if not id:
        return return_template('9-states.html')
    else:
        return render_template('9-states.html',
                               id=found_id,
                               name=name,
                               cities=cities)


@app.teardown_appcontext
def remove_session(exception=None):
    """remove current SQL Alcehmy session"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
