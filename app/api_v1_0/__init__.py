"""
Initialization script for restapi for the application.
"""

from flask import Blueprint

api = Blueprint('api', __name__)

from . import views, errors
