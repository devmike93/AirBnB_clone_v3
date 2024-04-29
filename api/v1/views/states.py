#!/usr/bin/python3
"""
A new view for 'States' - states.py
Handles all default RESTFul API actions
GET, POST, DELETE, PUT
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves list for all state objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_spec_state(state_id):
    """retrieves state information for specific state by ID"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a state object using state id
    DELETE /api/v1/states/<state_id>
    """
    state_del = storage.get("State", state_id)
    if state_del is None:
        abort(404)
    state_del.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """
    creates a new state object
    State: POST /api/v1/states
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """
    updates a state object
    PUT /api/v1/states/<state_id>
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
        if not request.is_json:
            raise ValueError('Not a JSON')
        for attrib, value in data.items():
            if attrib not in ['id', 'created_at', 'updated_at']:
                setattr(state, attrib, value)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    storage.save()
    return jsonify(state.to_dict())
