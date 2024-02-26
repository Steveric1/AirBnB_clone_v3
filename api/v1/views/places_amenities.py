#!/usr/bin/python3
""" Configures RESTful api for the places_amenities route """

from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


def get_place_and_amenity(place_id, amenity_id):
    """Retrieves Place and Amenity objects, handling errors."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if not place or not amenity:
        abort(404)

    return place, amenity


@app_views.route("places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_places_amenities(place_id):
    """Returns a list of amenities for a given place."""
    place = storage.get("Place", place_id)

    if not place:
        abort(404)

    amenities_dict = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_dict)


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["DELETE", "POST"], strict_slashes=False)
def manage_place_amenity(place_id, amenity_id):
    """Handles adding or removing an amenity from a place."""
    place, amenity = get_place_and_amenity(place_id, amenity_id)
    storage_type = getenv("HBNB_TYPE_STORAGE")

    if request.method == "DELETE":
        remove_amenity(place, amenity, storage_type)
    else:
        link_amenity(place, amenity, storage_type)

    return jsonify(amenity.to_dict()), 201


def remove_amenity(place, amenity, storage_type):
    """Removes an amenity from a place based on storage type."""
    if amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)

    storage.save()


def link_amenity(place, amenity, storage_type):
    """Links an amenity to a place based on storage type."""
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)

    storage.save()