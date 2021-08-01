"""beaconsfield.reddit

Module to call Reddit for images and to download them

Functions:
    get_top_wallpapers() -> List[str]
    download(str, str)
"""

from logging import info
from os.path import join
from re import compile as re_compile
from time import sleep
from typing import List

from requests import get

from beaconsfield.model import IMAGE_EXTENSION_PATTERN


URL = "https://www.reddit.com/r/wallpapers/hot.json"
HEADERS = {"User-agent": "Beaconsfield"}
API_SLEEP = 5


def get_top_wallpapers() -> List[str]:
    """Get the top URLs from the /r/wallpapers subreddit"""

    info("Calling %s for images" % URL)
    response = get(URL, headers=HEADERS).json()
    data = response["data"] if "data" in response else {}
    posts = data["children"] if "children" in data else []
    post_data = [post["data"] for post in posts if "data" in post]
    urls = [post["url"] for post in post_data if "url" in post]
    image_pattern = re_compile(IMAGE_EXTENSION_PATTERN)
    image_urls = [url for url in urls if image_pattern.fullmatch(url)]
    info("Got %d images from Reddit" % len(image_urls))
    return image_urls


def download(url: str, save_dir: str):
    """Download an image and store it in the save directory"""

    filename = join(save_dir, url.split("/")[-1])
    info("Downloading %s" % url)

    with open(filename, "wb") as file:
        with get(url, headers=HEADERS) as req:
            for chunk in req.iter_content(chunk_size=1024):
                file.write(chunk)

    info("Sleeping for %d secs before proceeding" % API_SLEEP)
    sleep(API_SLEEP)
