"""
Configuration file for the application.
"""
import os
from helpers.helper_functions import generate_secret_key
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secret_key()
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
