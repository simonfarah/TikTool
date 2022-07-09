import requests
from threading import Thread

from ._helpers import download, headers


class User:
    def __init__(self, username):
        req = requests.get(f"https://tiktok.com/@{username}")

        # check if the user exists
        # if the user does not exist -> we set the self.data to None
        # if the user exists -> we fetch the data related to the user
        if req.status_code == 404:
            self.data = None
        else:
            params = {"uniqueId": str(self.username)}
            self.data = requests.get(
                f"https://www.tiktok.com/api/user/detail",
                headers=headers(),
                params=params,
            ).json()

    def downloadAllVideos(self, watermark=True):
        """
        Download the published videos of a public user

        @param watermark (optional, default -> True)
        set the watermark to True to download videos with watermark
        set the watermark to False to download videos without watermark
        """

        # if the data is None which means that the user does not exist, we return False
        # if the user exists but is a private account, we return False
        if self.data is None or self.data["userInfo"]["user"]["privateAccount"]:
            return False

        # get the secUid of the user and make a request to the
        # Tiktok API to get the list of the user published videos
        sec_uid = self.data["userInfo"]["user"]["secUid"]
        params = {
            "sec_user_id": sec_uid,
            "count": "33",
            "device_id": "9999999999999999999",
            "max_cursor": "0",
            "aid": "1180",
        }
        data = requests.get(
            f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/post",
            headers=headers(),
            params=params,
        ).json()
        videos = data["aweme_list"]

        # download each video using a thread so we make
        # the process go faster
        for video in videos:
            download_url = video["video"][
                "download_addr" if watermark else "play_addr"
            ]["url_list"][0]

            download_path = "video.mp4"
            download_thread = Thread(
                target=download,
                args=(
                    download_url,
                    download_path,
                ),
            )
            download_thread.start()

        # return True when all the videos are downloaded
        return True

    def downloadProfilePicture(self):
        """
        Download the profile picture of a user
        """

        # if the data is None which means that the user does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["userInfo"]["user"]["avatarLarger"]
        download_path = "profile.jpeg"
        download(download_url, download_path)

        # return True when the profile picture is downloaded
        return True
