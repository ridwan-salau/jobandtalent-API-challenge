import requests
import os
import json

bearer_token = os.environ["BEARER_TOKEN"]


def create_user_by_id_url(usernames: list):
    # Specify the usernames that you want to lookup below
    usernames: str = ",".join(usernames)
    usernames = f"usernames={usernames}"
    url = f"https://api.twitter.com/2/users/by?{usernames}&user.fields=public_metrics"
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:

        # ::TO-DO:: Handle rate-limiting status-code 429. Response header has the reset time.
        
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
            )
    return response.json()


def get_twitter_prfiles(dev1: str, dev2: str):
    usernames = [dev1, dev2]
    
    url = create_user_by_id_url(usernames)
    json_response = connect_to_endpoint(url)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response

def create_follow_url(id: int, followers: bool=True, next_token=None, max_results=1000):
    url = f"https://api.twitter.com/2/users/{id}/" \
        f"{'followers' if followers else 'following'}" \
        f"?max_results={max_results}"
    if next_token:
        url = f"{url}&pagination_token={next_token}"
    return url

def get_twitter_follows(id, check_followers: bool, next_token=None, max_results=1000):
    url = create_follow_url(id, check_followers, next_token, max_results)
    response_json = connect_to_endpoint(url)
    return response_json

def is_ref_connected_to_source(source_id, reference_id, check_followers: bool = True, next_token=None):
    follows = get_twitter_follows(source_id, check_followers, next_token)

    for user_obj in follows["data"]:
        if user_obj["id"] == reference_id:
            return True
    else:
        next_token = follows["meta"].get("next_token")
        if next_token is None:
            return False
        else:
            is_ref_connected_to_source(source_id, reference_id, next_token)

def decide_follower_following(json_response: dict):
    dev1 = json_response["data"][0]
    dev2 = json_response["data"][1]

    combined_followers = dev1["public_metrics"]["followers_count"] + dev2["public_metrics"]["followers_count"]
    combined_following = dev1["public_metrics"]["following_count"] + dev2["public_metrics"]["following_count"]

    if combined_followers < combined_following:
        # print("Using followers list")
        return True
    # print("Using following list")
    return False

def devs_mutually_connected(dev1, dev2):

    json_response = get_twitter_prfiles(dev1, dev2)

    errors = json_response.get("errors")
    if errors:
        return {
            "connected":False, 
            "errors": [
                f"{error['value']} is not a valid user in twitter"
                for error in errors
            ]
        }

    check_followers = decide_follower_following(json_response)
    dev1_id = json_response["data"][0]["id"]
    dev2_id = json_response["data"][1]["id"]

    if is_ref_connected_to_source(source_id=dev1_id, reference_id=dev2_id, check_followers=check_followers) \
        and is_ref_connected_to_source(source_id=dev2_id, reference_id=dev1_id, check_followers=check_followers):

        return {"connected": True}
    else:
        return {"connected": False}



if __name__ == "__main__":
    usernames = ['ridzy619', 'ericokwechime']
    print(get_twitter_prfiles(*usernames))