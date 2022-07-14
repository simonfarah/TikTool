import requests

from ._helpers import headers


class Trending:
    def __init__(self):
        params = {"aid": "1988", "count": "30", "from_page": "fyp"}
        self.data = requests.get(
            "https://www.tiktok.com/node/share/discover/",
            headers=headers(),
            params=params,
        ).json()

    def users(self):
        """
        Get trending users
        """

        response = []

        for user in self.data["body"][0]["exploreList"]:
            response.append(
                {
                    "username": user["cardItem"]["subTitle"],
                    "nickname": user["cardItem"]["title"],
                    "bio": user["cardItem"]["description"],
                    "link": "https://tiktok.com" + user["cardItem"]["link"],
                    "id": user["cardItem"]["extraInfo"]["userId"],
                    "sec_uid": user["cardItem"]["extraInfo"]["secUid"],
                    "followers": user["cardItem"]["extraInfo"]["fans"],
                    "following": user["cardItem"]["extraInfo"]["following"],
                    "likes": user["cardItem"]["extraInfo"]["likes"],
                    "videos": user["cardItem"]["extraInfo"]["video"],
                    "verified": user["cardItem"]["extraInfo"]["verified"],
                    "liked_videos": user["cardItem"]["extraInfo"]["digg"],
                }
            )

        return response

    def hashtags(self):
        """
        Get trending hashtags
        """

        response = []

        for hashtag in self.data["body"][1]["exploreList"]:
            response.append(
                {
                    "hashtag": hashtag["cardItem"]["title"],
                    "name": hashtag["cardItem"]["extraInfo"]["challengeName"],
                    "description": hashtag["cardItem"]["description"],
                    "views": hashtag["cardItem"]["extraInfo"]["views"],
                    "id": hashtag["cardItem"]["extraInfo"]["challengeId"],
                    "link": "https://tiktok.com" + hashtag["cardItem"]["link"],
                }
            )

        return response

    def audio(self):
        """
        Get trending audio
        """

        response = []

        for audio in self.data["body"][2]["exploreList"]:
            response.append(
                {
                    "name": audio["cardItem"]["title"],
                    "owner_nickname": audio["cardItem"]["description"],
                    "link": "https://tiktok.com" + audio["cardItem"]["link"],
                    "id": audio["cardItem"]["extraInfo"]["musicId"],
                    "posts": audio["cardItem"]["extraInfo"]["posts"],
                    "download_stream_link": audio["cardItem"]["extraInfo"]["playUrl"],
                    "cover_image_link": audio["cardItem"]["cover"].replace(
                        "100x100", "1080x1080"
                    ),
                }
            )

        return response
