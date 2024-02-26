#!/usr/bin/python3

"""create a route /status on the object app_views
that returns a JSON: "status": "OK" """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Return a JSON status: OK"""
    return jsonify(status="OK")
