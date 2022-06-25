from flask_restful import Api, Resource

status_api = Api()

class Status(Resource):
    def get(self):
        return {
            "status":"green"
        }

status_api.add_resource(Status, "/")