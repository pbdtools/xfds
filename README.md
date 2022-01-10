# xFDS

Tool for e<u>x</u>ecuting FDS runs with [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles).

## Installation

To use xFDS, you must have the following installed on your workstation:

- [Docker](https://www.docker.com/): Needed to run fds-dockerfiles images
- [Python](https://www.python.org/): Needed to run pipx
- [pipx](https://pypa.github.io/pipx/): Needed to install xFDS

pipx allows you to install and run Python applications in isolated environments. This means that xFDS will be available anywhere on your machine and will not interfere with other Python projects or installations.

Once Docker, Python, and pipx are installed, install xFDS with the following command:

```
pipx install xfds
```

## License

xFDS is licensed under the [MIT License](https://opensource.org/licenses/MIT). FDS is public domain and fds-dockerfiles is released under the MIT License. Since this is a light wrapper for both projects, it only seems appropriate to release xFDS for public use.

## Usage

xfds [options] [fds_file]

### Options
- `-h`, `--help`: Display help dialogue
- `-i`, `--interactive`: Launch Docker container in interactive mode (`--it`). By default, the Docker image will run the FDS model, but interactive mode will put you into the container where you can start the FDS model manually. This is good for when you are rapidly iterating and don't want to wait for the Docker image load time.
- `-w`, `--windows`: Use a Windows Docker image. By default, xFDS assumes you want to use a Linux docker container. This will allow you to specify to use a Windows based container.
- `-n`, `--processors`: Specify number of processors. Defaults to 1 processor. If the number of processors is greater than 1, it will invoke MPI for you (`mpiexec -n #`). Ignored if interactive mode is enabled.

### Arguments:
- `fds_file`: The FDS file or directory to run.
  - If a **FDS file** is specified, the FDS model will run.
  - If a **directory** is specified, xFDS will find the first FDS file in the directory and assume that is what it should run. If no fds file exists, xFDS will default to interactive mode.
  - if **nothing** is specified, the current directory is used and the above rules are applied.

## Examples

The command used for running docker is based on the following logic:

- `docker run`: Start docker.
- `--rm`: Clean up after exit.
- `--it`: Interactive mode
- `--name <name>`: Name for running docker container. If a FDS file is specified, the base name of the FDS file is used. Otherwise, the FDS version is used.
- `-v <working directory>:<mounted directory>`: Mount directory inside container
  - Working directory determined based on `fds_file` argument.
  - `/workdir`: Mount directory in Linux Container.
  - `C:\workdir`: Mount directory in Windows Container.
- `openbcl/fds:<fds version>`: Container image to use. Defaults to latest.
- `mpiexec -n <meshcount>`: Use MPI if If `-n` > 1.
- `fds <fds_file>`: Run specified FDS file.

### When passing a FDS file
Run the specified FDS file.
```
/tests/data/fds$ xfds test.fds

docker run --rm --name test -v /tests/data/fds:/workdir openbcl/fds:<VERSION> fds test.fds
```
If interactive mode is requested, it will ignore the specified file, but mount the directory
```
/tests/data/fds$ xfds -i test.fds

docker run --rm -it --name fds-<VERSION> -v /tests/data/fds:/workdir openbcl/fds:<VERSION>
```
Run the specfied FDS file using a Windows image.
```
/tests/data/fds$ xfds -w test.fds

docker run --rm --name test -v /tests/data/fds:C:\workdir openbcl/fds:<VERSION> fds test.fds
```
Run the specified FDS file using 2 processors and MPI.
```
/tests/data/fds$ xfds -n 2 test.fds

docker run --rm --name test -v /tests/data/fds:/workdir openbcl/fds:<VERSION> mpiexec -n 2 fds test.fds
```
### When passing a directory containing an FDS file

Run the first FDS file in the current directory.
```
/tests/data/fds$ xfds

docker run --rm --name test -v /tests/data/fds:/workdir openbcl/fds:<VERSION> fds test.fds
```
Open the current directory in interactive mode.
```
/tests/data/fds$ xfds -i

docker run --rm -it --name fds-<VERSION> -v /tests/data/fds:/workdir openbcl/fds:<VERSION>
```
Run the first FDS file in the current directory using a Windows image.
```
/tests/data/fds$ xfds -w

docker run --rm --name test -v /tests/data/fds:C:\workdir openbcl/fds:<VERSION> fds test.fds
```
Run the first FDS file in the current directory using 2 processors and MPI.
```
/tests/data/fds$ xfds -n 2

docker run --rm --name test -v /tests/data/fds:/workdir openbcl/fds:<VERSION> mpiexec -n 2 fds test.fds
```

### When passing a directory not containing an FDS file
xFDS automatically enters interactive mode.
```
/tests/data/no_fds$ xfds

docker run --rm -it --name fds-6.7.7 -v /tests/data/no_fds:/workdir openbcl/fds:6.7.7
```
Interactive mode can be explicitly specified, but is not necessary.
```
/tests/data/no_fds$ xfds -i

docker run --rm -it --name fds-6.7.7 -v /tests/data/no_fds:/workdir openbcl/fds:6.7.7
```
Interactive mode using a Windows image.
```
/tests/data/no_fds$ xfds -w

docker run --rm -it --name fds-6.7.7 -v /tests/data/no_fds:C:\workdir openbcl/fds:6.7.7
```
