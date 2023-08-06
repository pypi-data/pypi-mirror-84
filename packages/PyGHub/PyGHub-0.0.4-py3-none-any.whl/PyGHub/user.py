import requests
from pyghub import Github
from pprint import pprint


class User(Github):
    def get_username(self):
        try:
            return self.user.json()["login"]
        except Exception as e:
            return e

    def get_user_id(self):
        try:
            return self.user.json()["id"]
        except Exception as e:
            return e

    def get_profile_url(self):
        try:
            return self.user.json()["html_url"]
        except Exception as e:
            return e
    
    def get_twitter_username(self):
        try:
            return self.user.json()["twitter_username"]
        except Exception as e:
            return e

    def get_avatar_url(self):
        try:
            return self.user.json()["avatar_url"]
        except Exception as e:
            return e

    def get_followers(self):
        try:
            followers = requests.get(f"{self.url}/user/followers", headers=self.headers)
            return followers.json()
        except Exception as e:
            return e
