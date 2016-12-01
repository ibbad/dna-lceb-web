"""
Initialization script for restapi for the application.
"""

from flask import Blueprint
from app.common.logging import setup_logging

api = Blueprint('api', __name__)

# Setup logger
# api_log = setup_logging(__name__, 'logs/api.log', maxFilesize=1000000,
#                         backup_count=5)

from . import views, errors
