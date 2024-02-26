#!/usr/bin/python3

from models.base_model import BaseModel
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request
from models.state import State
import os


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON object with the status"""
    return jsonify({"status": "OK"})


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns a list of all the State objects"""
    list_states = []
    for state in storage.all(State).values():
        list_states.append(state.to_dict())
    return jsonify(list_states)

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Returns a State object based on the state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object based on the state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State object"""
    data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    stateobj = State(data['name'])
    storage.new(stateobj)
    storage.save()
    return jsonify(stateobj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a State object"""
    if state_id is None:
        abort(404)
    response = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    update_state = storage.get(State, state_id)
    dict_ignore = ['id', 'created_at', 'updated_at']
    if update_state is None:
        abort(404)
    for key, value in response.items():
        if key not in dict_ignore:
            setattr(update_state, key, value)
    storage.save()
    return jsonify(update_state.to_dict()), 200
