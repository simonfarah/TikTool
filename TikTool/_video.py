import requests
from bs4 import BeautifulSoup

from ._helpers import download, headers


class Video:
    def __init__(self, link):
        req = requests.get(link, headers=headers())
        soup = BeautifulSoup(req.content, "html.parser")

        # check if the video exists (not using the status_code 404 because the
        # link provided might not be a video link and the status_code will be 200)
        # check for an element with a tag of "link" and attribute of rel="canonical"
        # that way we check if the link is a Tiktok video and is not private and
        # convert from mobile Tiktok video link to desktop Tiktok video link in one
        # go to get the video ID
        # if the link is to a public Tiktok video -> we fetch the data related to the video
        # if the link is not to a Tiktok video or if the video is private -> set self.data to None
        video_link = soup.find("link", attrs={"rel": "canonical"})
        if video_link is not None:
            self.video_id = video_link.get("href").split("/")[5]

            params = {"aweme_ids": f"[{self.video_id}]"}
            self.data = requests.get(
                f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/",
                headers=headers(),
                params=params,
            ).json()
        else:
            self.data = None

    def downloadVideo(self, watermark=True, path=None):
        """
        Download a public Tiktok video

        @param watermark (optional, default -> True)
        set the watermark to True to download video with watermark
        set the watermark to False to download video without watermark

        @param path (optional)
        set the download path of the file
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["video"][
            "download_addr" if watermark else "play_addr"
        ]["url_list"][0]

        download_path = path
        # if the download path was not passed
        if path is None:
            # define the default installation path
            download_path = f"./download/{self.video_id}/{'watermark' if watermark else 'no-watermark'}.mp4"

        download(download_url, download_path)

        # return True when the video is downloaded
        return True

    def downloadThumbnail(self, path=None):
        """
        Download the thumbnail of a public Tiktok video

        @param path (optional)
        set the download path of the file
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["video"]["origin_cover"][
            "url_list"
        ][0]

        download_path = path
        # if the download path was not passed
        if path is None:
            # define the default installation path
            download_path = f"./download/{self.video_id}/thumbnail.jpeg"

        download(download_url, download_path)

        # return True when the thumbnail is downloaded
        return True

    def downloadAudio(self, path=None):
        """
        Download the audio of a public Tiktok video

        @param path (optional)
        set the download path of the file
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["music"]["play_url"]["uri"]

        download_path = path
        # if the download path was not passed
        if path is None:
            # define the default installation path
            download_path = f"./download/{self.video_id}/audio.mp3"

        download(download_url, download_path)

        # return True when the audio is downloaded
        return True

    def downloadAudioCover(self, path=None):
        """
        Download the audio cover of a public Tiktok video

        @param path (optional)
        set the download path of the file
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["music"]["cover_large"][
            "url_list"
        ][0]

        download_path = path
        # if the download path was not passed
        if path is None:
            # define the default installation path
            download_path = f"./download/{self.video_id}/audio-cover.jpeg"

        download(download_url, download_path)

        # return True when the audio cover is downloaded
        return True

    def getDetails(self):
        """
        Get details/info of a public Tiktok video
        """

        # if the data is None which means that the video does not exist, we return None
        if self.data is None:
            return None

        shares_total = self.data["aweme_details"][0]["statistics"]["share_count"]
        shares_via_whatsapp = self.data["aweme_details"][0]["statistics"][
            "whatsapp_share_count"
        ]

        views_count = self.data["aweme_details"][0]["statistics"]["play_count"]
        downloads_count = self.data["aweme_details"][0]["statistics"]["download_count"]
        likes_count = self.data["aweme_details"][0]["statistics"]["digg_count"]
        comments_count = self.data["aweme_details"][0]["statistics"]["comment_count"]

        download_links_wm = self.data["aweme_details"][0]["video"]["download_addr"][
            "url_list"
        ]
        download_links_no_wm = self.data["aweme_details"][0]["video"]["play_addr"][
            "url_list"
        ]

        music_name = self.data["aweme_details"][0]["music"]["title"]
        music_owner_username = self.data["aweme_details"][0]["music"]["owner_handle"]
        music_owner_name = self.data["aweme_details"][0]["music"]["owner_nickname"]
        music_download_link = self.data["aweme_details"][0]["music"]["play_url"]["uri"]
        music_cover_image = self.data["aweme_details"][0]["music"]["cover_large"][
            "url_list"
        ][0]

        hashtags = []
        for hashtag in self.data["aweme_details"][0]["text_extra"]:
            hashtags.append(hashtag["hashtag_name"])

        return {
            "shares": {
                "total": shares_total,
                "shares_via_whatsapp": shares_via_whatsapp,
            },
            "views_count": views_count,
            "downloads_count": downloads_count,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "download": {
                "wm": download_links_wm,
                "no-wm": download_links_no_wm,
            },
            "music": {
                "name": music_name,
                "owner_username": music_owner_username,
                "owner_name": music_owner_name,
                "download_link": music_download_link,
                "cover_image": music_cover_image,
            },
            "hashtags": hashtags,
        }
