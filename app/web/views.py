"""
This module implements view functions for web application.
"""
from . import web
from flask import flash, redirect, render_template, url_for, abort, request, \
    current_app
from app.common import find_coding_region, find_capacity_for_coding_region


@web.route('/shutdown')
def server_shutdown():
    """
    Shutdown application server.
    :return:
    """
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@web.index('/')
def index():
    # TODO: redirect to project index page.
    return redirect(url_for('web.embed'))

