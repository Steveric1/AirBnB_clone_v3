#!/usr/bin/python3

"""create a route /status on the object app_views
that returns a JSON: "status": "OK" """
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "amenities": "Amenity", "cities": "City",
        "places": "Place", "reviews": "Review",
        "states": "State", "users": "User"
    }
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
