#!/usr/bin/python3
"""Users view module"""

from models.user import User
from models import storage
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from flasgger import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    user = storage.all(User)
    list_users = []
    for user in user.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/users/get_user_by_id.yml', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/users/delete_user_by_id.yml', methods=['DELETE'])
def delete_user_by_id(user_id):
    """Delete user object based on id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    user.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/users/post_users.yml', methods=['POST'])
def posting():
    """Create user object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    amenity_obj = User(**data)
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/users/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
