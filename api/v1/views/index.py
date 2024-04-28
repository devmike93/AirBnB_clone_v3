#!/usr/bin/python3
"""index holds endpoint to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnb_options = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns current status of API in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns number of objects in options"""
    stats_dict = {}
    for key, value in hbnb_options.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)

if __name__ == "__main__":
    pass
