"""beaconsfield.storage

Module to interact with the storage directory

Functions:
    get_saved_wallpapers(str) -> List[str]
"""

from logging import info
from os import listdir
from os.path import join
from re import compile as re_compile
from typing import List


from beaconsfield.model import IMAGE_EXTENSION_PATTERN


def _get_path_images(path: str) -> List[str]:
    image_pattern = re_compile(IMAGE_EXTENSION_PATTERN)
    all_files = listdir(path)
    all_images = [file for file in all_files if image_pattern.fullmatch(file)]
    info("Loaded %d images from %s" % (len(all_images), path))
    return all_images


def get_saved_wallpapers(storage_dir: str) -> List[str]:
    """Returns a list of paths if they are images"""
    return [join(storage_dir, f) for f in _get_path_images(storage_dir)]
