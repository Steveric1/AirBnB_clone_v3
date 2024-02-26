#!/usr/bin/python3
"""City objects that handles all default
RestFul API actions"""

from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views


app_views.route('/states/<state_id>/cities', methods=['GET'],
                strict_slashes=False)


def get_cities(state_id):
    """Returns a list of all the City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = []
    cities = storage.all(City)

    for city in cities.values():
        if city.state_id == state_id:
            list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a City object based on the city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object based on the city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    cityobj = City(**data)
    cityobj.state_id = state_id
    cityobj.save()
    return make_response(jsonify(cityobj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
