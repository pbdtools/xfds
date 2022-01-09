"""Default settings."""
INTERACTIVE: bool = False
LINUX: bool = True
WINDOWS: bool = False
PROCESSORS: int = 1

NIX = "linux"
WIN = "windows"
WSL = "wsl"
VERSIONS = {
    "6.2.0": {NIX: True, WSL: True, WIN: False},
    "6.3.0": {NIX: True, WSL: True, WIN: False},
    "6.5.3": {NIX: True, WSL: True, WIN: True},
    "6.6.0": {NIX: True, WSL: False, WIN: True},
    "6.7.0": {NIX: True, WSL: False, WIN: True},
    "6.7.1": {NIX: True, WSL: True, WIN: False},
    "6.7.3": {NIX: True, WSL: True, WIN: True},
    "6.7.4": {NIX: True, WSL: True, WIN: True},
    "6.7.5": {NIX: True, WSL: True, WIN: True},
    "6.7.6": {NIX: True, WSL: True, WIN: True},
    "6.7.7": {NIX: True, WSL: True, WIN: False},
}
LATEST: str = list(VERSIONS.keys())[-1]
