import requests
import os


def download(url, path):
    # get the file name and extension
    file_name = os.path.basename(path)
    # get the path without the name and extension of the file
    path_without_file_name = path[: -len(file_name)]

    if path_without_file_name == "":
        pass
    else:
        os.makedirs(path_without_file_name, exist_ok=True)

    with open(path, "wb") as out_file:
        item_bytes = requests.get(url, stream=True)
        out_file.write(item_bytes.content)


def headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Cookie": "msToken=zgbEqIjfSC7M7QdTTpHDkpWLtnY4JnK22HiSE1iHCRGBBYY_36Gm-gMDqyGLBjpPE2svzjVPNGWyMFYUUEBwmGkr5y2qQuKmfjfTh0i2hfOsb_B7jfDrbd9a4IhjMLPyUIRNIZLqzG6PldNNXA==",
    }

    return headers
