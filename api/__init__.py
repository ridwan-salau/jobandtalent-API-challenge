import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config_by_name

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object( config_by_name[config_name])
    db.init_app(app)

    migrate = Migrate(app, db)

    from api.controller.routes import api_blueprint
    from api.controller import status_api

    status_api.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix="/connected/")


    return app