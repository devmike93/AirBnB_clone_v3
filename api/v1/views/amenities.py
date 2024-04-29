#!/usr/bin/python3
"""states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    retrieves information for all amenities
    GET /api/v1/amenities
    """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """
    retrieves information for specified amenity
    GET /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_amenity(amenity_id):
    """
    deletes an amenity based on its amenity_id
    DELETE /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    creates a new amenity
    POST /api/v1/amenities
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    updates an amenity
    PUT /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
        if not request.is_json:
            raise ValueError('Not a JSON')
        for attrib, value in data.items():
            if attrib not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, attrib, value)
    except ValueError as e:
        return make_response(jsonify({'error': str(e)}), 400)
    amenity.save()
    return jsonify(amenity.to_dict())
