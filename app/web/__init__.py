"""
Initialization script for web application.
"""

from flask import Blueprint

web = Blueprint('web', __name__)

from . import views, errors
