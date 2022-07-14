import requests
from threading import Thread

from ._helpers import download, headers


class User:
    def __init__(self, username):
        self.username = username
        req = requests.get(f"https://tiktok.com/@{username}")

        # check if the user exists
        # if the user does not exist -> we set the self.data to None
        # if the user exists -> we fetch the data related to the user
        if req.status_code == 404:
            self.data = None
        else:
            params = {"uniqueId": str(self.username)}
            self.data = requests.get(
                "https://www.tiktok.com/api/user/detail/",
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
            "https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/post/",
            headers=headers(),
            params=params,
        ).json()
        videos = data["aweme_list"]

        # download each video using a thread so we make
        # the process go faster
        count = 0
        for video in videos:
            count += 1
            download_url = video["video"][
                "download_addr" if watermark else "play_addr"
            ]["url_list"][0]

            download_path = f"./download/{self.username}/{'watermark' if watermark else 'no-watermark'}-{count}.mp4"
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

    def downloadProfilePicture(self, path=None):
        """
        Download the profile picture of a user

        @param path (optional)
        set the download path of the file
        """

        # if the data is None which means that the user does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["userInfo"]["user"]["avatarLarger"]

        download_path = path
        # if the download path was not passed
        if path is None:
            # define the default installation path
            download_path = f"./download/{self.username}/profile.jpeg"

        download(download_url, download_path)

        # return True when the profile picture is downloaded
        return True

    def getDetails(self):
        """
        Get details/info of a Tiktok user
        """

        # if the data is None which means that the user does not exist, we return None
        if self.data is None:
            return None

        id = self.data["userInfo"]["user"]["id"]
        sec_uid = self.data["userInfo"]["user"]["secUid"]
        nickname = self.data["userInfo"]["user"]["nickname"]
        is_verified = self.data["userInfo"]["user"]["verified"]
        is_private_account = self.data["userInfo"]["user"]["privateAccount"]
        is_under_18 = self.data["userInfo"]["user"]["isUnderAge18"]
        profile_picture = self.data["userInfo"]["user"]["avatarLarger"]
        following_count = self.data["userInfo"]["stats"]["followingCount"]
        follower_count = self.data["userInfo"]["stats"]["followerCount"]
        video_count = self.data["userInfo"]["stats"]["videoCount"]
        likes_count = self.data["userInfo"]["stats"]["heart"]
        liked_videos_count = self.data["userInfo"]["stats"]["heartCount"]
        bio_text = self.data["userInfo"]["user"]["signature"]
        try:
            bio_link = self.data["userInfo"]["user"]["bioLink"]["link"]
            bio_link_risk = self.data["userInfo"]["user"]["bioLink"]["risk"]
        except KeyError:
            bio_link = ""
            bio_link_risk = 0

        return {
            "id": id,
            "sec_uid": sec_uid,
            "nickname": nickname,
            "is_verfied": is_verified,
            "is_private_account": is_private_account,
            "is_under_18": is_under_18,
            "profile_picture": profile_picture,
            "stats": {
                "following_count": following_count,
                "follower_count": follower_count,
                "video_count": video_count,
                "likes_count": likes_count,
                "liked_videos_count": liked_videos_count,
            },
            "bio": {
                "bio_text": bio_text,
                "bio_link": bio_link,
                "bio_link_risk": bio_link_risk,
            },
        }
