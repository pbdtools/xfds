from enum import Enum


class Service(Enum):
    FDS = "fds"
    DOCKER = "images"


class Location(Enum):
    LOCAL = "local"
    SABALCORE = "sabalcore"
