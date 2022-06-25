import json
from math import floor
import os
import time
from cryptography.hazmat.primitives import serialization
import jwt
import requests

pem_path = os.environ["JOBANDTALENT_PEM_PATH"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
USERNAME = "ridzy619"

with open(pem_path, "rb") as r:
    private_pem = r.read()
private_key = serialization.load_pem_private_key(private_pem, password=None)

iat = floor(time.time())
token = {
    # issued at time, 60 seconds in the past to allow for clock drift
    "iat": iat,
    # JWT expiration time (10 minute maximum)
    "exp": iat + 10 * 60,
    # GitHub App's identifier
    "iss": 211840,
}

encoded_jwt = jwt.encode(token, private_key, algorithm="RS256")
# print(encoded_jwt)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {encoded_jwt}"
    r.headers["Accept"] = "application/vnd.github.v3+json"
    return r


def token_oauth(r):
    r.headers["Authorization"] = f"token {GITHUB_ACCESS_TOKEN}"
    r.headers["Accept"] = "application/vnd.github.v3+json"
    return r


def connect_to_endpoint(url, auth=bearer_oauth):
    response = requests.request(
        "GET",
        url,
        auth=auth,
    )
    if response.status_code == 404:
        return {"error": "{dev_username} is not a valid user in github"}
    if response.status_code != 200:
        return f"Request returned an error: {response.status_code} {response.text}"
    return response.json()


def create_user_orgs_list_url(username, page=1):
    return f"https://{USERNAME}:{GITHUB_ACCESS_TOKEN}@api.github.com/users/{username}/orgs?per_page=100&page={page}"


def get_orgs_id_list(username, page=1):
    url = create_user_orgs_list_url(username, page)
    response_json = connect_to_endpoint(url, auth=None)

    if len(response_json) == 100:
        return response_json + get_orgs_id_list(username, page + 1)

    return response_json


def devs_have_common_orgs(dev1, dev2):
    dev1_orgs_response = get_orgs_id_list(dev1)
    dev2_orgs_response = get_orgs_id_list(dev2)
    print(dev1_orgs_response, dev2_orgs_response)

    errors = []
    if isinstance(dev1_orgs_response, dict) and dev1_orgs_response.get("error"):
        errors.append(dev1_orgs_response["error"].format(dev_username=dev1))
    if isinstance(dev2_orgs_response, dict) and dev2_orgs_response.get("error"):
        errors.append(dev2_orgs_response["error"].format(dev_username=dev2))

    if errors:
        return {"connected": False, "errors": errors}

    dev1_orgs = [org["id"] for org in dev1_orgs_response]
    dev2_orgs = [org["id"] for org in dev2_orgs_response]

    common_orgs = set(dev1_orgs).intersection(dev2_orgs)
    if common_orgs:
        return {
            "connected": True,
            "organisations": [
                org["login"] for org in dev1_orgs_response if org["id"] in common_orgs
            ],
        }

    return {
        "connected": False,
    }


if __name__ == "__main__":
    username = "ridzy61900"
    devs = ["earowanrg", "mitchelloharawilde"]
    # url = f"https://api.github.com/users/{username}/followers"
    # url = f"https://api.github.com/app/installations"
    # url = "https://api.github.com/app/installations/26614705/access_token"

    # print(url)
    # print(json.dumps(connect_to_endpoint(url), indent=4))

    print(devs_have_common_orgs(*devs))

    # url = create_user_orgs_list_url(username)
    # print(url)
    # print(json.dumps(connect_to_endpoint(url, auth=None), indent=4))
