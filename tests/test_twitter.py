import unittest
from tests.test_base import BaseCase
from api.service.twitter import *


class TestTwitter(unittest.TestCase):
    def test_twitter_followers(self):

        followers = get_twitter_follows(224975323, check_followers=True)

        self.assertEqual(len(followers["data"]), 116, "Follower count test failed")

    def test_twitter_following(self):

        followerings = get_twitter_follows(224975323, check_followers=False)

        self.assertEqual(len(followerings["data"]), 266, "Following count failed")

    def test_decide_followers_following_True(self):
        json_response = {
            "data": [
                {
                    "name": "Ridwan Salahuddeen",
                    "id": "224975323",
                    "public_metrics": {
                        "followers_count": 116,
                        "following_count": 266,
                        "tweet_count": 957,
                        "listed_count": 0,
                    },
                    "username": "Ridzy619",
                },
                {
                    "name": "Ifeanyichukwu Okwechime",
                    "id": "1538141948954935297",
                    "public_metrics": {
                        "followers_count": 20,
                        "following_count": 45,
                        "tweet_count": 0,
                        "listed_count": 0,
                    },
                    "username": "ericokwechime",
                },
            ]
        }

        check_followers = decide_follower_following(json_response)

        self.assertTrue(
            check_followers, "decide_follower_following failed to return True"
        )

    def test_decide_followers_following_False(self):
        json_response = {
            "data": [
                {
                    "name": "Ridwan Salahuddeen",
                    "id": "224975323",
                    "public_metrics": {
                        "followers_count": 116,
                        "following_count": 266,
                        "tweet_count": 957,
                        "listed_count": 0,
                    },
                    "username": "Ridzy619",
                },
                {
                    "name": "Ifeanyichukwu Okwechime",
                    "id": "1538141948954935297",
                    "public_metrics": {
                        "followers_count": 200,
                        "following_count": 45,
                        "tweet_count": 0,
                        "listed_count": 0,
                    },
                    "username": "ericokwechime",
                },
            ]
        }

        check_followers = decide_follower_following(json_response)

        self.assertFalse(
            check_followers, "decide_follower_following failed to return False"
        )

    def test_create_follow_url(self):
        id = "224975323"
        url_actual = "https://api.twitter.com/2/users/224975323/followers?max_results=50&pagination_token=somerandomtoken"
        url = create_follow_url(
            id, followers=True, next_token="somerandomtoken", max_results=50
        )

        self.assertEqual(url, url_actual)

        url_actual = "https://api.twitter.com/2/users/224975323/following?max_results=50&pagination_token=somerandomtoken"
        url = create_follow_url(
            id, followers=False, next_token="somerandomtoken", max_results=50
        )

        self.assertEqual(url, url_actual)

    def test_is_ref_connected_to_source(self):
        dev1 = "224975323"
        dev2 = "1538141948954935297"
        is_connected = is_ref_connected_to_source(
            dev1,
            dev2,
            True,
        )

        self.assertTrue(is_connected, "Failed connection test using followers lists")

        dev1 = "224975323"
        dev2 = "1538141948954935297"
        is_connected = is_ref_connected_to_source(
            dev1,
            dev2,
            False,
        )

        self.assertTrue(is_connected, "Failed connection test using following lists")

        dev1 = "224975323"
        dev2 = "1538141948954935298"
        is_connected = is_ref_connected_to_source(
            dev1,
            dev2,
            True,
        )

        self.assertFalse(is_connected, "Failed connection test using followers lists")

        dev1 = "224975323"
        dev2 = "1538141948954935298"
        is_connected = is_ref_connected_to_source(
            dev1,
            dev2,
            True,
        )

        self.assertFalse(is_connected, "Failed connection test using following lists")

    def test_devs_mutually_connected(self):
        test_list = [
            {
                "input": {"dev1": "ridzy619", "dev2": "ericokwechime"},
                "exp_output": {"connected": True},
            },
            {
                "input": {"dev1": "ridzy619", "dev2": "ericokwechimeee"},
                "exp_output": {
                    "connected": False,
                    "errors": ["ericokwechimeee is not a valid user in twitter"],
                },
            },
            {
                "input": {"dev1": "ridzy6190000000", "dev2": "ericokwechimeee"},
                "exp_output": {
                    "connected": False,
                    "errors": [
                        "ridzy6190000000 is not a valid user in twitter",
                        "ericokwechimeee is not a valid user in twitter",
                    ],
                },
            },
            {
                "input": {"dev1": "ridzy619", "dev2": "Hafusay"},
                "exp_output": {"connected": False},
            },
        ]
        dev1 = "ridzy619"
        dev2 = "ericokwechime"

        response = devs_mutually_connected(dev1, dev2)

        for test_dict in test_list:
            input = test_dict["input"]
            exp_output = test_dict["exp_output"]
            output = devs_mutually_connected(**input)
            self.assertEqual(output, exp_output, "Error!!!")
