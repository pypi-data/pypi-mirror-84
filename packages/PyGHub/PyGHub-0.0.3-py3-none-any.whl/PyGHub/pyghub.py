import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


class Github:
    """The main class."""
    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.url = "https://api.github.com"
        self.headers = {
                'Authorization': f'token {self.token}',
                'owner': f'{self.username}',
            }

    def get_user_data(self):
        """This method get the user data that you want and return a json
        with this data."""
        try:
            user = requests.get(f'{self.url}/user', headers=self.headers)
            return user.json()
        except Exception as e:
            return e

    def get_repos_data(self):
        """This method get the repositories data from the user and return a
        json with this data."""
        try:
            repos = requests.get(
                f"{self.url}/users/owner/repos", headers=self.headers)
            return repos.json()
        except Exception as e:
            return e

    def get_repo_data(self, repo):
        try:
            obtained_repo = requests.get(
                f"{self.url}/repos/{self.username}/{repo}", headers=self.headers)
            return obtained_repo.json()
        except Exception as e:
            return e


github = Github(username="FRostri", token="50175f7706b34335b3d742750314044060e2e38c")
pprint(github.get_repo_data("PyGHub"))
