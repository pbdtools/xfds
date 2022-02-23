[![Tests](https://github.com/pbdtools/xfds/workflows/Tests/badge.svg)](https://github.com/pbdtools/xfds/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/pbdtools/xfds/main/graph/badge.svg)](https://codecov.io/gh/pbdtools/xfds)
[![PyPI](https://img.shields.io/pypi/v/xfds.svg)](https://pypi.org/project/xfds)

# xFDS

Tool for executing FDS runs with [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles).

Do you have FDS installed on your machine? Do you know where the FDS executable is located? Do you know what version it is? If you installed FDS and Pathfinder, you might have multiple versions of FDS on your machine, but which one do you use?

xFDS leverages the power of Docker to give you acess to all the versions of FDS without having to manage the different versions of FDS yourself. Best of all, you don't have to change or install anything when FDS has a new release!

Once xFDS is installed, all you have to do is navigate to your file and type `xfds`. It will locate the first FDS file in the directory and run it with the latest version of FDS!

```
~/tests/data/fds$ ls
test.fds
~/tests/data/fds$ xfds
docker run --rm --name test-1b6d0d27-2cce-4555-a827-4b31d0e03215 -v /tests/data/fds:/workdir openbcl/fds:6.7.7 fds test.fds
```

## Usage

xfds [options] [fds_file]

### Options
- `-h`, `--help`: Display help dialogue
- `-i`, `--interactive`: Launch Docker container in interactive mode (`--it`). By default, the Docker image will run the FDS model, but interactive mode will put you into the container where you can start the FDS model manually. This is good for when you are rapidly iterating and don't want to wait for the Docker image load time.
- `-v`, `--version`: Specify FDS version to use. The FDS version can also be extracted from the file path or metadata in the FDS file.
- `-n`, `--processors`: Specify number of processors. Defaults to 1 processor. If the number of processors is greater than 1, it will invoke MPI for you (`mpiexec -n #`). Ignored if interactive mode is enabled.
- `--fds-versions`: List FDS versions available on Docker Hub and exit. See [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles) for compatability information.

### Arguments:
- `fds_file`: The FDS file or directory to run.
  - If a **FDS file** is specified, the FDS model will run.
  - If a **directory** is specified, xFDS will find the first FDS file in the directory and assume that is what it should run. If no fds file exists, xFDS will default to interactive mode.
  - if **nothing** is specified, the current directory is used and the above rules are applied.

## Features

**Auto-detect FDS file in directory**

If you're in a directory containing an FDS file, xFDS will find the FDS file without you specifying what file to run. This is best when each FDS model has its own directory. If multiple FDS files are in the directory, only the first file found will be executed.

If no FDS file is found, xFDS will put you into an interactive session with the directory mounted inside the Docker container. If no directory is specified, the current working directory will be used.

**Latest version of FDS always available.**

xFDS will always default to the latest version thanks to how the Docker images are created, but you're always welcome to use an older version of FDS if needed. See [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles) for supported versions.

**Always know what FDS version you're using.**

xFDS will inject the FDS version into the container name so there's no question what version of FDS is running. xFSD will also append a globally unique ID so there's no conflicts in having multipe containers running.

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
