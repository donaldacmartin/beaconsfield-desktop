"""beaconsfield.sys

Module to handle interactions with the underlying operating system

Functions:
    check_sys(str)
    set_wallpaper(str)
"""

import ctypes

from logging import debug, info
from os import access, listdir, remove, system, R_OK, W_OK
from os.path import isdir, join
from platform import system as platform_sys

from beaconsfield.model import SysException


ACCEPTABLE_SYSTEMS = ["Linux", "Darwin", "Windows"]


def _check_os() -> bool:
    debug("Checking that OS is compatible")
    operating_system = platform_sys()
    debug("OS is %s" % operating_system)

    if operating_system in ACCEPTABLE_SYSTEMS:
        return True

    raise SysException("Unacceptable OS: %s" % operating_system)


def _check_dir(storage_dir: str) -> bool:
    debug("Checking that %s is a writable directory" % storage_dir)

    if isdir(storage_dir) and access(storage_dir, R_OK | W_OK):
        return True

    raise SysException("%s is not a writable directory" % storage_dir)


def check_sys(storage_dir: str):
    """Check that OS acceptable & storage directory is writable"""

    info("Checking system")
    return _check_os() and _check_dir(storage_dir)


def clear_dir(storage_dir: str):
    """Wipe out the old wallpapers"""

    info("Clearing out %s" % storage_dir)
    images = listdir(storage_dir)
    paths = [join(storage_dir, image) for image in images]
    info("Deleting %d file(s)" % len(paths))
    list(map(remove, paths))


def set_wallpaper(wallpaper: str):
    """Set the wallpaper using the underlying OS call"""

    info("Setting wallpaper to %s" % wallpaper)
    operating_system = platform_sys()

    if operating_system == "Windows":
        debug("Windows detected")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 3)
    elif operating_system == "Linux":
        debug("Linux detected")
        system("gsettings set org.gnome.desktop.background picture-uri %s" % wallpaper)
    else:
        raise SysException("Cannot set wallpapers on %s" % operating_system)
