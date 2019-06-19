from flask import Flask
from .extensions import mongo
from .main import main
from flask_jwt_extended import JWTManager


def create_app(config_object="ivr-ns-rest.settings"):
    application = Flask(__name__)

    application.config.from_object(config_object)

    mongo.init_app(application)

    application.register_blueprint(main)

    jwt = JWTManager(application)

    return application
