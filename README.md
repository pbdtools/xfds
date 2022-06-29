

![Last Commit](https://img.shields.io/github/last-commit/pbdtools/xfds)
[![Tests](https://github.com/pbdtools/xfds/workflows/Tests/badge.svg)](https://github.com/pbdtools/xfds/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/pbdtools/xfds/main/graph/badge.svg)](https://codecov.io/gh/pbdtools/xfds)

![Python](https://img.shields.io/pypi/pyversions/xfds.svg)
![Implementation](https://img.shields.io/pypi/implementation/xfds)
![License](https://img.shields.io/github/license/pbdtools/xfds.svg)

[![PyPI](https://img.shields.io/pypi/v/xfds.svg)](https://pypi.org/project/xfds)
![Development Status](https://img.shields.io/pypi/status/xfds)
![Wheel](https://img.shields.io/pypi/format/xfds)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xfds)

Source Code: [github.com/pbdtools/xfds](https://github.com/pbdtools/xfds)

Documentation: [xfds.pbd.tools](https://xfds.pbd.tools)


![xFDS Logo](https://raw.githubusercontent.com/pbdtools/xfds/main/docs/assets/xfds_logo_lg.png)

Do you have FDS installed on your machine? Do you know where the FDS executable is located? Do you know what version it is? If you installed FDS and Pathfinder, you might have multiple versions of FDS on your machine, but which one do you use?

xFDS leverages the power of Docker to give you acess to all the versions of FDS without having to manage the different versions of FDS yourself. Best of all, you don't have to change or install anything when FDS has a new release!

Once xFDS is installed, all you have to do is navigate to your file and type `xfds run`. It will locate the first FDS file in the directory and run it with the latest version of FDS!

```
~/tests/data/fds$ ls
test.fds
~/tests/data/fds$ xfds run
docker run --rm --name test -v /tests/data/fds:/workdir openbcl/fds fds test.fds
```

## Features

### Generate Parametric Analyses

Fire models can often require mesh sensitivity studies, different fire sizes, multiple exhaust rates, and a number of differnt parameters. With the power of the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) templating system, xFDS can help generate a variety of models from a single `.fds` file!

**Specify Resolution, not `IJK`**

Let xFDS calculate the number of cells so you don't have to. By setting variables at the top of your FDS file, you can use them to perform calculations. Variables are defined using the [MultiMarkdown Specification](https://fletcherpenney.net/multimarkdown/#metadata) for file metadata. Expressions between curly braces `{` and `}` are evaluated as Python code.

```
xmax: 5
ymax: 4
zmax: 3
res: 0.1

&MESH XB=0, {xmax}, 0, {ymax}, 0, {zmax}, IJK={xmax // res}, {ymax // res}, {zmax // res}/
```

Will translate to:

```
&MESH XB= 0, 5, 0, 4, 0, 3, IJK= 50, 40, 30/
```

Want to run a coarser mesh? Just change `res` to `0.2` and get

```
&MESH XB= 0, 5, 0, 4, 0, 3, IJK= 25, 20, 15/
```

**Use loops to create an array of devices**

Create [for loops](https://jinja.palletsprojects.com/en/3.1.x/templates/#for) by typing `{% for item in list %} ... {% endfor %}`.

```
{% for x in range(1, 5) %}
{% for y in range(1, 3) %}
&DEVC QUANTITY='TEMPERATURE', IJK={x}, {y}, 1.8/
{% endfor %}
{% endfor %}
```

Will render to the following code. Note, [Python's `range()`](https://docs.python.org/3.3/library/stdtypes.html?highlight=range#range) function will exclude the upper bound.

```
&DEVC QUANTITY='TEMPERATURE', IJK=1, 1, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=1, 2, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=2, 1, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=2, 2, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=3, 1, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=3, 2, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=4, 1, 1.8/
&DEVC QUANTITY='TEMPERATURE', IJK=4, 2, 1.8/
```


### Manage FDS Runs

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
xFDS depends on the following softwares:

- [Docker](https://www.docker.com/): Needed to run fds-dockerfiles images
- [Python](https://www.python.org/): Needed to run pipx
- [pipx](https://pypa.github.io/pipx/): Needed to install xFDS

Once Docker, Python, and pipx are installed, install xFDS with the following command:

```
pipx install xfds
```

For more information about installing xFDS, see https://xfds.pbd.tools/installation


<a href="https://xfds.pbd.tools" style="font-size: 2em; text-align: center; padding: 1em; border: 1px solid #444; display: block; color: rgb(255, 110, 66);">
Learn more at xfds.pbd.tools
</a>
