"""
Initialization for application main package.
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config

# instantiate modules
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    """
    This function creates the application instance for the dna-lceb
    :param config_name: key loading configuration from Config file.
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize modules
    bootstrap.init_app(app)
    moment.init_app(app)

    # Register blueprint for web app. and restapi.
    from .web import web as web_blueprint
    app.register_blueprint(web_blueprint)

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, prefix='/api/v1.0/')

    return app
