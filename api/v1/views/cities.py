#!/usr/bin/python3
"""cities.py"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    get city information for all cities in a specified state
    GET /api/v1/states/<state_id>/cities
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_dict = []
    cities_dict = [city.to_dict() for city in state.cities_dict]
    return jsonify(cities_dict)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_city(city_id):
    """
    retrieves city information for specific city
    GET /api/v1/states/<state_id>/cities
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_city(city_id):
    """
    deletes a city based on its city_id
    DELETE /api/v1/cities/<city_id>
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_a_city(state_id):
    """
    create a new city
    POST /api/v1/states/<state_id>/cities
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_one_city(city_id):
    """
    updates a city according to specified id

    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
        if not request.is_json:
            raise ValueError('Not a JSON')
        for attrib, value in data.items():
            if attrib not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, attrib, value)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    city.save()
    return jsonify(city.to_dict())
