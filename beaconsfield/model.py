"""beaconsfield.model

Stores the structure for the application

Constants:
    LOG_FORMAT
    IMAGE_EXTENSION_PATTERN

Classes:
    BeaconsfieldException
    SysException
"""

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
IMAGE_EXTENSION_PATTERN = ".+\\.((jpg)|(jpeg)|(png)|(bmp))"


class BeaconsfieldException(Exception):
    """Generic exception from which everything should be subclassed"""


class SysException(BeaconsfieldException):
    """Exceptions thrown while interacting with the OS"""
