#!/usr/bin/python3
"""objects that handle all default RestFul"""

from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_review(place_id):
    """Retrieves the list of all review objects of a place"""
    place_rev = storage.get(Place, place_id)
    if not place_rev:
        abort(404)
    list_reviews = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review_id(review_id):
    """Retrieves a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_review.yml', methods=['POST'])
def rev_posting(place_id):
    """Creates a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    data = request.get_json()
    user_id = storage.get(User, data['user_id'])

    if not user_id:
        abort(404)

    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/reviews/put_review.yml', methods=['PUT'])
def put_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
