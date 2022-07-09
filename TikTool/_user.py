import requests
from _helpers import download, headers


class User:
    def __init__(self, username):
        req = requests.get(f"https://tiktok.com/@{username}")

        # check if the user exists
        # if the user does not exist -> we set the self.data to None
        # if the user exists -> we fetch the data related to the user
        if req.status_code == 404:
            self.data = None
        else:
            params = {
                "device_id": "7098862702289995269",
                "uniqueId": str(self.username),
            }
            self.data = requests.get(
                f"https://www.tiktok.com/api/user/detail",
                headers=headers(),
                params=params,
            ).json()
