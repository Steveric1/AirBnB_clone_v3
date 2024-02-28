#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response
from os import environ
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places_amenities/get_amenities.yml')
def get_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def delete(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    a_id = storage.get(Amenity, amenity_id)
    if not a_id:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        if a_id not in p_id.amenities:
            abort(404)
        p_id.amenities.remove(a_id)
    else:
        if amenity_id not in p_id.amenity_ids:
            abort(404)
        p_id.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def posting(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    p_id = storage.get(Place, place_id)
    if not p_id:
        abort(404)
    a_id = storage.get(Amenity, amenity_id)
    if not a_id:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        if a_id in p_id.amenities:
            return make_response(jsonify(a_id.to_dict()), 200)
        p_id.amenities.append(a_id)
    else:
        if amenity_id in p_id.amenity_ids:
            return make_response(jsonify(a_id.to_dict()), 200)
        p_id.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(a_id.to_dict()), 201)
