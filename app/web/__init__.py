"""
Initialization script for web application.
"""

from flask import Blueprint
from app.common.logging import setup_logging

web = Blueprint('web', __name__)

# Setup logger
# web_log = setup_logging(__name__, 'logs/web.log', maxFilesize=1000000,
#                         backup_count=5)

from . import views, errors
