#!/usr/bin/python3
"""places.py"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    retrieves for all places in a specified city
    GET /api/v1/cities/<city_id>/places
    """
    try:
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    deletes a place based on its place_id
    DELETE /api/v1/places/<place_id>
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_place(place_id):
    """
    get place information for specified place
    GET /api/v1/places/<place_id>
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    updates a place
    PUT /api/v1/places/<place_id>
    """
    try:
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        data = request.get_json()
        if not data:
            raise ValueError('Not a JSON')
        for attrib, value in data.items():
            if attrib not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, attrib, value)
        place.save()
        return jsonify(place.to_dict())
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create a new place
    POST /api/v1/cities/<city_id>/places
    """
    try:
        city = storage.get("City", city_id)
        if city is None:
            abort(404)
        data = request.get_json()
        if not data:
            raise ValueError('Not a JSON')
        if 'user_id' not in data:
            raise ValueError('Missing user_id')
        user = storage.get("User", data['user_id'])
        if user is None:
            abort(404)
        if 'name' not in data:
            raise ValueError('Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

"""
ADVANCED
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def update_place_search():
    """"""
    searches for a place

    """"""
    try:
        params = request.get_json()
        if not params:
            raise ValueError('Not a JSON')
        
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])

        amenity_objects = [storage.get('Amenity', amenity_id) for amenity_id in amenities]

        places = []
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                places.extend(place for city in state.cities for place in city.places if city.id in cities)

        confirmed_places = []
        for place in places:
            if all(amenity in place.amenities for amenity in amenity_objects):
                confirmed_places.append(place.to_dict())

        return jsonify(confirmed_places)

    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
"""