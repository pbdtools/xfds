# Installation

## Install xFDS

Once you have Python and pipx installed on your machine (see below), you can install xFDS with the following command.

```console title="Install xFDS"
$ pipx install xfds
```

You can verify that xfds is working by displaying the help text. If this does not work, try [troubleshooting pipx](https://pypa.github.io/pipx/troubleshooting/)

```console title="Print Help"
$ xfds --help
```


## Required Third Party Packages

### Python

[Python](https://www.python.org/) is a high-level general-purpose programming language. If you don't have Python installed on your machine, it is recommended that you get the latest stable version of the Python interpreter. [Real Python](https://realpython.com) has a nice [article](https://realpython.com/installing-python/) to help you get Python on your machine.

**How does xFDS use Python?**

xFDS is written in Python! You will need a Python interpreter for xFDS to run.

### pipx

[pipx](https://pypa.github.io/pipx/) allows you to install python applications in isolated envrionments. To install pipx, check out their [installation instructions](https://pypa.github.io/pipx/installation/)

**How does xFDS use pipx?**

While you could use [pip](https://pip.pypa.io/en/stable/) to install xFDS, it could interfere with the Python version your machine uses to function. pipx is the recommended way to install xFDS on your machine.

### Docker

[Docker](https://www.docker.com/) is a platform used to develop and deliver software in packages called containers. These containers are lightweight computing environment that use the host computer's resources, while isolating the running container from the host machine.

Docker can be installed on most modern computers. For instructions on how to setup Docker, visit their [getting started](https://www.docker.com/get-started/) page.

**How does xFDS use Docker?**

The generous folks at [BCL](https://web.bcl-leipzig.de/) have developed a series of Docker images for a variety of FDS versions. The images are maintained under a [MIT License](https://opensource.org/licenses/MIT) on [Github](https://github.com/openbcl/fds-dockerfiles) and available for use on [dockerhub](https://hub.docker.com/r/openbcl/fds).

To run a multi-core model in a docker image, the user would have to enter the following command into their terminal:

```console title="Docker Run Command"
docker run --rm -v $(pwd):/workdir openbcl/fds mpiexec -n 2 fds casename.fds
```

The xFDS [run command](commands/run.md) simplifies this command and will automatically locate the FDS input file in the current directory with the following command:
```console title="xFDS Run Command"
xfds run -n 2
```

If you don't intend to use the [run command](commands/run.md) for running tests locally, you can skip this step.

**What's the difference between pipx and Docker?**
Docker will isolate the container from the rest of the host machine and does not have access to the host machine unless specified. With xFDS, the docker containers only have access to read and write from the specified directory, but cannot interface with the host machines systems and services.

In contrast, pipx isolates the dependencies for xFDS from other Python projects on the host machine. It makes xFDS available on the command line anywhere on the host machine.
