"""beaconsfield.beaconsfield

The main application

Functions:
    refresh_images(str, int)
    set_new_wallpaper(str)
    main(str, str, int)
"""

from argparse import ArgumentParser
from logging import INFO, basicConfig, info, error
from os.path import basename
from pathlib import Path
from random import randint
from typing import List

from beaconsfield.model import LOG_FORMAT, BeaconsfieldException
from beaconsfield.reddit import download, get_top_wallpapers
from beaconsfield.storage import get_saved_wallpapers
from beaconsfield.sys import check_sys, set_wallpaper


DEFAULT_DIR = Path.home()
DEFAULT_NUM = 10


def _filter_saved_wps(saved_wps: List[str], reddit_wps: List[str]) -> List[str]:
    saved_names = [basename(wp) for wp in saved_wps]
    return [wp for wp in reddit_wps if wp.split("/")[-1] not in saved_names]


def refresh_images(storage_dir: str, num_wallpapers: int):
    """Call Reddit for new wallpapers and put them in the provided directory"""

    try:
        info("Refreshing images")
        check_sys(storage_dir)
        saved_wallpapers = get_saved_wallpapers(storage_dir)
        top_wallpapers = get_top_wallpapers()
        new_wallpapers = _filter_saved_wps(saved_wallpapers, top_wallpapers)
        map(lambda x: download(x, storage_dir), new_wallpapers[:num_wallpapers])
    except BeaconsfieldException as beaconsfield_exception:
        error(beaconsfield_exception)


def set_new_wallpaper(storage_dir: str):
    """Choose a random wallpaper from the provided directory"""

    try:
        info("Setting a new wallpaper")
        check_sys(storage_dir)
        all_wallpapers = get_saved_wallpapers(storage_dir)
        random_wallpaper = all_wallpapers[randint(0, len(all_wallpapers) - 1)]
        set_wallpaper(random_wallpaper)
    except BeaconsfieldException as beaconsfield_exception:
        error(beaconsfield_exception)


def main(action: str, storage_dir: str, num_wallpapers: int):
    """The main application"""

    if action == "set":
        set_new_wallpaper(storage_dir)
    elif action == "refresh":
        refresh_images(storage_dir, num_wallpapers)
    else:
        error("Unknown action %s" % action)


if __name__ == "__main__":
    basicConfig(format=LOG_FORMAT, level=INFO)
    parser = ArgumentParser()

    parser.add_argument("--action", type=str, required=True, help="set|refresh")

    parser.add_argument(
        "--storage-dir",
        type=str,
        help="Where we can save wallpapers",
        default=DEFAULT_DIR,
    )

    parser.add_argument(
        "--num-wallpapers",
        type=int,
        help="How many wallpapers to download",
        default=DEFAULT_NUM,
    )

    args = parser.parse_args()
    main(args.action.lower(), args.storage_dir, args.num_wallpapers)
