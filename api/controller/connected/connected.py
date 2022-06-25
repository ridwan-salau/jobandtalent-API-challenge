from flask_restful import Resource

from api.service.register_data import get_register_data, save_register_data

from ...service.github import devs_have_common_orgs
from ...service.twitter import devs_mutually_connected


class RealTime(Resource):
    def _is_connected(self, dev1, dev2):
        github_connected_response = devs_have_common_orgs(dev1, dev2)
        twitter_connected_response = devs_mutually_connected(dev1, dev2)
        print(github_connected_response, twitter_connected_response)
        errors = []
        if github_connected_response.get("errors"):
            errors.extend(github_connected_response["errors"])
        if twitter_connected_response.get("errors"):
            errors.extend(twitter_connected_response["errors"])

        if errors:
            return {"errors": errors}

        elif (
            github_connected_response["connected"]
            and twitter_connected_response["connected"]
        ):

            return {
                "connected": True,
                "organisations": github_connected_response["organisations"],
            }

        return {"connected": False}

    def get(self, dev1, dev2):
        connected_data = self._is_connected(dev1, dev2)

        # Save data in the DB
        save_register_data(dev1, dev2, register_data=connected_data)
        # connected_data = {"response": "OK"}

        return connected_data


class Register(Resource):
    def get(self, dev1, dev2):
        register_data = get_register_data(dev1, dev2)
        # register_data = {"response": "OK"}

        return register_data
