[![Tests](https://github.com/pbdtools/xfds/workflows/Tests/badge.svg)](https://github.com/pbdtools/xfds/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/pbdtools/xfds/main/graph/badge.svg)](https://codecov.io/gh/pbdtools/xfds)
![Last Commit](https://img.shields.io/github/last-commit/pbdtools/xfds)

![Python](https://img.shields.io/pypi/pyversions/xfds.svg)
![Implementation](https://img.shields.io/pypi/implementation/xfds)
![License](https://img.shields.io/github/license/pbdtools/xfds.svg)

[![PyPI](https://img.shields.io/pypi/v/xfds.svg)](https://pypi.org/project/xfds)
![Development Status](https://img.shields.io/pypi/status/xfds)
![Wheel](https://img.shields.io/pypi/format/xfds)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xfds)


# xFDS

Tool for executing FDS runs with [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles).

![Docker](https://img.shields.io/docker/pulls/openbcl/fds?label=openbcl%2Ffds%20pulls&logo=docker)

Do you have FDS installed on your machine? Do you know where the FDS executable is located? Do you know what version it is? If you installed FDS and Pathfinder, you might have multiple versions of FDS on your machine, but which one do you use?

xFDS leverages the power of Docker to give you acess to all the versions of FDS without having to manage the different versions of FDS yourself. Best of all, you don't have to change or install anything when FDS has a new release!

Once xFDS is installed, all you have to do is navigate to your file and type `xfds run`. It will locate the first FDS file in the directory and run it with the latest version of FDS!

```
~/tests/data/fds$ ls
test.fds
~/tests/data/fds$ xfds run
docker run --rm --name test-1b6d0d27-2cce-4555-a827-4b31d0e03215 -v /tests/data/fds:/workdir openbcl/fds:6.7.7 fds test.fds
```

## Usage

Run `xfds --help` to see available commands. For help on a specific command, run `xfds <command> --help`. See [USAGE.md](https://github.com/pbdtools/xfds/blob/main/USAGE.md) for more.

## Features

**Auto-detect FDS file in directory**

If you're in a directory containing an FDS file, xFDS will find the FDS file without you specifying it. This is best when each FDS model has its own directory. If multiple FDS files are in the directory, only the first file found will be executed.

If no FDS file is found, xFDS will put you into an interactive session with the directory mounted inside the Docker container. If no directory is specified, the current working directory will be used.

**Latest version of FDS always available.**

xFDS will always default to the latest version thanks to how the Docker images are created, but you're always welcome to use an older version of FDS if needed. See [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles) for supported versions.

**Always know what FDS version you're using.**

xFDS will inject the FDS version into the container name so there's no question what version of FDS is running. xFDS will also append a globally unique ID so there's no conflicts in having multipe containers running.

**Runs in Background**

Fire and forget. Unless you use the interactive mode, xFDS will run your model in a container and free up the terminal for you to keep working.

## Installation

### Prerequisites
To use xFDS, you must have the following installed on your workstation:

- [Docker](https://www.docker.com/): Needed to run fds-dockerfiles images
- [Python](https://www.python.org/): Needed to run pipx
- [pipx](https://pypa.github.io/pipx/): Needed to install xFDS

Docker will allow you to run any suported version of FDS without installing it on your machine.

pipx allows you to install and run Python applications in isolated environments. This means that xFDS will be available anywhere on your machine and will not interfere with other Python projects or installations.

### Install xFDS
Once Docker, Python, and pipx are installed, install xFDS with the following command:

```
pipx install xfds
```

## License

xFDS is licensed under the [MIT License](https://opensource.org/licenses/MIT). FDS is public domain and fds-dockerfiles is released under the MIT License. Since this is a light wrapper for both projects, it only seems appropriate to release xFDS for public use.
