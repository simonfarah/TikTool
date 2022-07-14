## Available Features

- [x] Download videos with watermark
- [x] Download videos without watermark
- [x] Download video thumbnail
- [x] Download audio from video
- [x] Download audio cover from video
- [x] Get details/info about a video
- [x] Download all videos published by a user with watermark
- [x] Download all videos published by a user without watermark
- [x] Download user profile picture

## Installation

TikTool is just a tool for my other projects and is still unreleased, but contributions to the project are highly appreciated.
Install the module using the following command to test it out and help us develop the project further.

```bash
pip install "git+https://github.com/simonfarah/TikTool.git#egg=TikTool"
```

## Usage

- ### Video Related Functions

  #### Main setup

  ```python
  from TikTool import Video

  video = Video("https://www.tiktok.com/@tiktok/video/xxxxxxxxxx")

  # all link formats are accepted
  ```

  #### Download video with or without watermark

  ```python
  # download video with watermark
  video.downloadVideo(watermark=True, path="video.mp4")

  # download video without watermark
  video.downloadVideo(watermark=False, path="C:/Users/user/Desktop/video.mp4")

  # if the watermark parameter was not passed,
  # it will be set to True by default

  # if the path parameter was not passed,
  # you will find the downloaded video in the following path :
  # "./download/the_video_id/"
  ```

  Extra checks : this function will return `True` if the video was downloaded successfully and `False` if the video does not exist, is private or if the video was not downloaded.

  #### Download video thumbnail

  ```python
  # download video thumbnail
  video.downloadThumbnail(path="thumbnail.jpeg")

  # if the path parameter was not passed,
  # you will find the downloaded thumbnail in the following path :
  # "./download/the_video_id/"
  ```

  Extra checks : this function will return `True` if the thumbnail was downloaded successfully and `False` if the video does not exist, is private or if the thumbnail was not downloaded.

  #### Download audio from video

  ```python
  # download audio from video
  video.downloadAudio(path="audio.mp3")

  # if the path parameter was not passed,
  # you will find the downloaded audio in the following path :
  # "./download/the_video_id/"
  ```

  Extra checks : this function will return `True` if the audio was downloaded successfully and `False` if the video does not exist, is private or if the audio was not downloaded.

  #### Download audio cover from video

  ```python
  # download audio cover from video
  video.downloadAudioCover(path="audio-cover.jpeg")

  # if the path parameter was not passed,
  # you will find the downloaded audio cover in the following path :
  # "./download/the_video_id/"
  ```

  Extra checks : this function will return `True` if the audio cover was downloaded successfully and `False` if the video does not exist, is private or if the audio cover was not downloaded.

  #### Get video details/info

  ```python
  # get global details about video
  video.getDetails()
  ```

  Extra checks : this function will return `None` if the video does not exist or is private. Response structure (`object`):

  ```python
  {
      "shares": {
          "total": TOTAL_SHARES,
          "shares_via_whatsapp": TOTAL_SHARES_VIA_WHATSAPP
      },
      "views_count": VIDEO_VIEWS_COUNT,
      "downloads_count": VIDEO_DOWNLOADS_COUNT,
      "likes_count": VIDEO_LIKES_COUNT,
      "comments_count": VIDEO_COMMENTS_COUNT,
      "download": {
          "wm": [LIST OF DOWNLOAD LINKS - WITH WATERMARK],
          "no-wm": [LIST OF DOWNLOAD LINKS - WITHOUT WATERMARK]
      },
      "music": {
          "name": MUSIC_NAME,
          "owner_username": MUSIC_OWNER_USERNAME,
          "owner_name": MUSIC_OWNER_NAME,
          "download_link": MUSIC_DOWNLOAD_LINK,
          "cover_image": MUSIC_COVER_IMAGE_DOWNLOAD_LINK
      },
      "hashtags": [LIST OF HASHTAGS]
  }
  ```

- ### User Related Funtions

  #### Main setup

  ```python
  from TikTool import User

  user = User("username")
  ```

  #### Download user published videos with or without watermark

  ```python
  # download all the user published videos (with watermark)
  user.downloadAllVideos(watermark=True)

  # download all the user published videos (without watermark)
  user.downloadAllVideos(watermark=False)

  # if the watermark parameter was not passed,
  # it will be set to True by default

  # you will find the downloaded videos in the following path :
  # "./download/username/"
  ```

  Extra checks : this function will return `True` if the videos were downloaded successfully and `False` if the user does not exist, is a private account or if the videos were not downloaded.

  #### Download the user profile picture

  ```python
  # download the user profile picture
  user.downloadProfilePicture(path="profile.jpeg")

  # if the path parameter was not passed,
  # you will find the downloaded profile picture in the following path :
  # "./download/username/"
  ```

  Extra checks : this function will return `True` if the profile picture was downloaded successfully and `False` if the user does not exist, is a private account or if the profile picture was not downloaded.

  #### Get user details/info

  ```python
  # get global details about a user
  user.getDetails()
  ```

  Extra checks : this function will return `None` if the user does not exist. Response structure (`object`):

  ```python
  {
    "id": USER_ID,
    "sec_uid": USER_SEC_ID,
    "nickname": USER_NICKNAME,
    "is_verfied": USER_VERIFIED_STATUS,
    "is_private_account": USER_ACCOUNT_PRIVACY_STATUS,
    "is_under_18": USER_UNDER_18,
    "profile_picture": USER_PROFILE_PICTURE_DOWNLOAD_LINK,
    "stats": {
        "following_count": FOLLOWING_COUNT,
        "follower_count": FOLLOWERS_COUNT,
        "video_count": PUBLISHED_VIDEOS_COUNT,
        "likes_count": LIKES_COUNT,
        "liked_videos_count": LIKED_VIDEOS_COUNT, # WILL BE 0 IF LIKED VIDEOS ARE PRIVATE
    },
    "bio": {
        "bio_text": BIO_TEXT,
        "bio_link": THE_LINK_IN_BIO,
        "bio_link_risk": LINK_RISKINESS_LEVEL
    }
  }
  ```

- ### Trending Related Functions

  #### Main setup

  ```python
  from TikTool import Trending

  trending = Trending()
  ```

  #### Get trending users

  ```python
  # get trending users
  trending.users()
  ```

  Response structure (`object`):

  ```python
  [
    {
        "username": USERNAME,
        "nickname": NICKNAME,
        "bio": USER_BIO,
        "link": USER_PROFILE_LINK,
        "id": USER_ID,
        "sec_uid": USER_SEC_UID,
        "followers": FOLLOWERS_COUNT,
        "following": FOLLOWING_COUNT,
        "likes": LIKES_COUNT,
        "videos": PUBLISHED_VIDEOS_COUNT,
        "verified": USER_VERIFIED_STATUS,
        "liked_videos": LIKED_VIDEOS_COUNT
    },
    {
        ...
    }
  ]
  ```

  #### Get trending hashtags

  ```python
  # get trending hashtags
  trending.hashtags()
  ```

  Response structure (`object`):

  ```python
  [
    {
        "hashtag": HASHTAG,
        "name": HASHTAG_NAME,
        "description": HASHTAG_DESCRIPTION,
        "views": HASHTAG_VIEWS,
        "id": HASHTAG_ID,
        "link": HASHTAG_LINK
    },
    {
        ...
    }
  ]
  ```

  #### Get trending audio

  ```python
  # get trending audio
  trending.audio()
  ```

  Response structure (`object`):

  ```python
  [
    {
        "name": AUDIO_NAME,
        "owner_nickname": OWNER_NAME,
        "link": AUDIO_LINK,
        "id": AUDIO_ID,
        "posts": NUMBER_OF_POSTS_USING_THE_AUDIO,
        "download_stream_link": LINK_TO_DOWNLOAD_STREAM,
        "cover_image_link": LINK_TO_COVER_IMAGE
    },
    {
        ...
    }
  ]
  ```
