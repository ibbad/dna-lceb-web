"""
This module provides the errors handling for web application.
"""

from flask import render_template, request, jsonify
from . import web


@web.app_errorhandler(404)
def page_not_found(e):
    """
    Generate web api level error handlers for 404 errors. Checks for return
    type and generates response according i.e. html or json response.
    :param e: Error object.
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('errors/404.html'), 404


@web.app_errorhandler(500)
def internal_server_error(e):
    """
    Generate web api level error handlers for 500 errors. Checks for return
    type and generates response according i.e. html or json response.
    :param e: Error object.
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('errors/500.html',
                           error_message='Internal server error'), 500
