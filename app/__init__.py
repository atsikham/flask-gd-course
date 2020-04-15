import os
import configparser
import logging

from distutils.util import strtobool
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(environment):
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read('./config.ini')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()),
                                                                        config[environment]['database_name'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = strtobool(config['flask']['track_modifications'])
    app.config['JWT_SECRET_KEY'] = config['flask']['secret']
    app.logger.setLevel(logging.INFO)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    with app.app_context():
        from app.routes import routes
        from app.models import animal
        from app.models import center
        from app.models import species
        from app.models import api_access
    return app


def create_test_app():
    return create_app(environment='staging')


def create_production_app():
    return create_app(environment='production')


file_logger = logging.getLogger(__name__)
log_format_str = '[%(asctime)s] %(method_type)s %(req_url)s {center: %(center_id)d} {%(entity_type)s: %(entity_id)d}'
formatter = logging.Formatter(log_format_str)
file_handler = logging.FileHandler('filtered.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
file_logger.addHandler(file_handler)
