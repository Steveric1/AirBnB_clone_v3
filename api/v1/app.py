#!/usr/bin/python3
"""Create a new Flask app instance."""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

# Declare a method to teardown the app
@app.teardown_appcontext
def teardown_db(self):
    """Closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
