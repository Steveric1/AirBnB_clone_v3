#!/usr/bin/python3
"""Import blueprint"""

from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

# Wildcard import everything in the package of api.v1.views.index
from api.v1.views.index import *
