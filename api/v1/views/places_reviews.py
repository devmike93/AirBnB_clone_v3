#!/usr/bin/python3
"""
Create a new view for Review object - reviews.py
Handles all default RESTFul API actions
"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    retrieves reviews for a specified place by id
    GET /api/v1/places/<place_id>/reviews
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """
    deletes a review based on its review_id
    DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_review(review_id):
    """
    retrieves information for specified review
    GET /api/v1/reviews/<review_id>
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    creates a new review
    POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user_id = req_data.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    text = req_data.get('text')
    if not text:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    req_data['place_id'] = place_id
    review = Review(**req_data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    updates a review
    PUT /api/v1/reviews/<review_id>
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attrib, value in req_data.items():
        if attrib not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, attrib, value)
    review.save()
    return jsonify(review.to_dict())
