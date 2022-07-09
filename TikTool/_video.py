import requests
from bs4 import BeautifulSoup

from _helpers import download, headers


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
            video_id = video_link.get("href").split("/")[5]

            params = {"aweme_ids": f"%5B{video_id}%5D"}
            self.data = requests.get(
                f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail",
                headers=headers(),
                params=params,
            ).json()
        else:
            self.data = None

    def downloadVideo(self, watermark=True):
        """
        Download a public Tiktok video

        @param watermark (optional, default -> True)
        set the watermark to True to download video with watermark
        set the watermark to False to download video without watermark
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["video"][
            "download_addr" if watermark else "play_addr"
        ]["url_list"][0]
        download_path = "video.mp4"
        download(download_url, download_path)

        # return True when the video is downloaded
        return True

    def downloadThumbnail(self):
        """
        Download the thumbnail of a public Tiktok video
        """

        # if the data is None which means that the video does not exist, we return False
        if self.data is None:
            return False

        download_url = self.data["aweme_details"][0]["video"]["origin_cover"][
            "url_list"
        ][0]
        download_path = "thumbnail.jpeg"
        download(download_url, download_path)

        # return True when the thumbnail is downloaded
        return True
