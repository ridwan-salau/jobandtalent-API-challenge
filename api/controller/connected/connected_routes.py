from flask import Blueprint
from flask_restful import Api

from .connected import RealTime, Register

connected_bp = Blueprint("connected", __name__)

api = Api(connected_bp)

api.add_resource(RealTime, "/realtime/<string:dev1>/<string:dev2>/")
api.add_resource(Register, "/register/<string:dev1>/<string:dev2>/")
