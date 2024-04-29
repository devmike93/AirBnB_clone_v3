#!/usr/bin/python3
"""users.py"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    retrieves information for all users
    GET /api/v1/users
    """
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_user(user_id):
    """
    retrieves information for specified user
    GET /api/v1/users/<user_id>
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
    deletes a user based on its user_id
    DELETE /api/v1/users/<user_id>
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))

@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """
    updates a user entry
    PUT /api/v1/users/<user_id>
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    try:
        data = request.get_json()
        if not request.is_json:
            raise ValueError('Not a JSON')
        for attrib, value in data.items():
            if attrib not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, attrib, value)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    user.save()
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    creates a new user
    POST /api/v1/users
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)

