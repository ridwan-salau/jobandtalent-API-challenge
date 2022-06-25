from flask import Blueprint
from flask_restful import Api

from .connected.connected_routes import connected_bp


api_blueprint = Blueprint("api", __name__)

api = Api(api_blueprint)

# api.init_app(connected_bp)

api_blueprint.register_blueprint(
    connected_bp,
)
