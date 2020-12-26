import requests
from functools import lru_cache
from datetime import datetime, timedelta
from .config import Config


class Reddit(Config):
    def __init__(self):
        self.token_expire = None

    @property
    @lru_cache()
    def _auth_token(self):
        auth_endpoint = "https://www.reddit.com/api/v1/access_token"
        data = {
            "grant_type": "password",
            "username": self.USERNAME,
            "password": self.PASSWORD,
        }
        auth = requests.auth.HTTPBasicAuth(self.APP_ID, self.APP_SECRET)
        headers = {"user-agent": f"{self.APP_NAME} by {self.USERNAME}"}
        r = requests.post(auth_endpoint, data=data, headers=headers, auth=auth)
        status_code = r.status_code
        assert status_code == 200, status_code
        response = r.json()
        self.token_expire = datetime.now() + timedelta(
            seconds=response.get("expires_in")
        )
        return response.get("access_token")

    @property
    def _headers(self):
        if self.token_expire and (datetime.now() - self.token_expire).seconds < 3:
            Auth.auth_token.fget.cache_clear()
        return {
            "user-agent": f"{self.APP_NAME} by {self.USERNAME}",
            "Authorization": f"bearer {self._auth_token}",
        }

    def get(self, endpoint):
        r = requests.get(endpoint, headers=self._headers)
        return r

reddit = Reddit()


    