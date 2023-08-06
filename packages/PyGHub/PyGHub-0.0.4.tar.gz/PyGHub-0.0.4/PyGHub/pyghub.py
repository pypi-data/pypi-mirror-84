import requests

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
        self.user = requests.get(f"{self.url}/user", headers=self.headers)
