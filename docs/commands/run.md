# Run Command

The xFDS run command is a convience wrapper for docker run. xFDS determines the appropriate arguments for the model and exectues the docker run command for you.

Unless stated otherwise, the commands below assume you are at `/home/pbdtools/models` with the following directory structure.
```console
/home/pbdtools/models $ tree
.
├── multi_mesh # More than 1 processor required
│   └── multi_mesh.fds
│
├── multiple_files # Multiple fds files in directory
│   ├── model_01.fds
│   └── model_02.fds
│
└── single_mesh # Only 1 processor required
    └── single_mesh.fds
```



## Working in Different Shells

The `xfds run` command simplifies and unifies what you have to type into the terminal. The sytax for using FDS Dockerfiles without xFDS is sligntly different depending on what shell you're using. Each shell has it's own way of referring to the current directory.

- Linux / Mac - Bash
`$(pwd)`
- Windows Powershell
`${pwd}`
- Windows Command Prompt
`%cd%`

You can see the differences in the command syntaxes.

=== "Docker - Bash"
    ```console
    docker run --rm -v $(pwd):/workdir openbcl/fds fds <filename>.fds
    ```
=== "Docker - Powershell"
    ```console
    docker run --rm -v ${pwd}:/workdir openbcl/fds fds <filename>.fds
    ```
=== "Docker - Command Prompt"
    ```console
    docker run --rm -v %cd%:/workdir openbcl/fds fds <filename>.fds
    ```

xFDS eliminates this concern by using the absolute path in place of the shortcuts for the current directory. While generating the command to execute Docker, xFDS will also name the Docker container based on the file name and FDS version.

For example, if you're in `/home/pbdtools/models/single_mesh`, executing `xfds run` will have the output below.

```console title="xFDS Command"
xfds run
```
```console title="xFDS Output"
docker run --rm --name single_mesh-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest fds single_mesh.fds
```

For the rest of the examples, the xFDS command will be shown, and you can tab over to the equivalent Docker command as follows. The current directory will also be shown.

=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm --name single_mesh-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest fds single_mesh.fds
    ```

## Single vs Multiple Processors

The only difference between running a single processor model and a MPI processor is supplying the number of processors desired with the `-n` flag. xFDS will automatically call `mpiexec` if needed.

**Single processor**
=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm --name single_mesh-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest fds single_mesh.fds
    ```

**Two processors**
=== "xFDS"
    ```console title="/home/pbdtools/models/multi_mesh/"
    xfds run -n 2
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/multi_mesh/"
    docker run --rm --name multi_mesh-latest -v /home/pbdtools/models/multi_mesh:/workdir openbcl/fds:latest mpiexec -n 2 fds multi_mesh.fds
    ```

## Running From Different Directories

**From same directory as the fds file**
=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm --name single_mesh-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest fds single_mesh.fds
    ```

**From a parent directory**
=== "xFDS"
    ```console title="/home/pbdtools/models/"
    xfds run single_mesh
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/"
    docker run --rm --name single_mesh-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest fds single_mesh.fds
    ```

**Multiple files in the same directory**

If there are multiple fds files in the directory, xFDS will default to the first one.

=== "xFDS"
    ```console title="/home/pbdtools/models/multiple_files/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/multiple_files/"
    docker run --rm --name model_01-latest -v /home/pbdtools/models/multiple_files:/workdir openbcl/fds:latest fds model_01.fds
    ```

If you want to run `model_02.fds`, you must specify it.

=== "xFDS"
    ```console title="/home/pbdtools/models/multiple_files/"
    xfds run model_02.fds
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/multiple_files/"
    docker run --rm --name model_01-latest -v /home/pbdtools/models/multiple_files:/workdir openbcl/fds:latest fds model_02.fds
    ```

## Specifying FDS Version

FDS Dockerfiles supports most versions of FDS. xFDS will default to the latest version. If you would like to specify an older version you can pass the desired version to xFDS. See the [fds-dockerfiles repo](https://github.com/openbcl/fds-dockerfiles) for information on supported versions.

These examples will pretend like you want to run FDS 6.7.5. xFDS will use the `openbcl/fds:6.7.5` image and FDS version will be appended to the container name. This way it is clear what model and version are running.

These subsections also indicate the priority of different methods. Specifying a version on the command line will take the highest precidence while a version in the file path will be the lowest priority.

### Command Line Argument

=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run -v 6.7.5
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm --name single_mesh-6.7.5 -v /home/cohan/github/pbdtools/models/single_mesh:/workdir openbcl/fds:6.7.5 fds single_mesh.fds
    ```

### File Metadata

xFDS supports metadata in FDS input files via the [MultiMarkdown Specification](https://fletcherpenney.net/multimarkdown/#metadata). If you want to ensure a file is always run with the same version of FDS, you can specify a `fds` keyword at the top of the file and xFDS will call the appropriate container.

This method has the benefit of documenting the intended version of FDS for a model which can be useful if you are returning to a project after a while. Furthermore, this prevents your models from unexpectedly running on a different version if a new version of FDS is released mid project.

```console title="/home/pbdtools/models/single_mesh/single_mesh.fds"
fds: 6.7.5
---
&MESH /
```

=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm --name single_mesh-6.7.5 -v /home/cohan/github/pbdtools/models/single_mesh:/workdir openbcl/fds:6.7.5 fds single_mesh.fds
    ```

### File Path

xFDS will read the full path to the model and determine if a folder is specifying a version of FDS. The version can use periods (`.`) or underscores (`_`) and may be preceeded by either `fds` or `v`. The following paths are equivalent and all run FDS 6.7.5.

```
/home/pbdtoos/models/6.7.5/single_mesh/single_mesh.fds
/home/pbdtoos/models/v6.7.5/single_mesh/single_mesh.fds
/home/pbdtoos/models/v.6.7.5/single_mesh/single_mesh.fds
/home/pbdtoos/models/fds6.7.5/single_mesh/single_mesh.fds
/home/pbdtoos/models/fds.6.7.5/single_mesh/single_mesh.fds

/home/pbdtoos/models/6_7_5/single_mesh/single_mesh.fds
/home/pbdtoos/models/v6_7_5/single_mesh/single_mesh.fds
/home/pbdtoos/models/v_6_7_5/single_mesh/single_mesh.fds
/home/pbdtoos/models/fds6_7_5/single_mesh/single_mesh.fds
/home/pbdtoos/models/fds_6_7_5/single_mesh/single_mesh.fds
```

=== "xFDS"
    ```console title="/home/pbdtools/models/6.7.5/single_mesh/"
    xfds run
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/6.7.5/single_mesh/"
    docker run --rm --name single_mesh-6.7.5 -v /home/cohan/github/pbdtools/models/6.7.5/single_mesh:/workdir openbcl/fds:6.7.5 fds single_mesh.fds
    ```

This method is particularly useful if you have tests that you need to run on different versions. You can copy the entire directory over, rename the version folder, and then all the models will use that new version.

## Interactive Mode

Interactive mode is useful if you need to quickly iterate on a given model, but don't want to incur the startup cost for the container. To enter interactive mode, pass the `-i` flag to xFDS.

=== "xFDS"
    ```console title="/home/pbdtools/models/single_mesh/"
    xfds run -i
    ```
=== "Docker"
    ```console title="/home/pbdtools/models/single_mesh/"
    docker run --rm -it --name fds-latest -v /home/pbdtools/models/single_mesh:/workdir openbcl/fds:latest
    ```

This will put you in a terminal inside the container.

```console title="Inside Container"
root@00a83c3c6390:/workdir# pwd
/workdir
root@00a83c3c6390:/workdir# ls
single_mesh.fds
root@00a83c3c6390:/workdir# fds

 Fire Dynamics Simulator

 Current Date     : June 23, 2022  19:44:42
 Revision         : FDS6.7.8-0-gfbf3e11ee-release
 Revision Date    : Tue May 24 18:07:45 2022 -0400
 Compiler         : ifort version 2021.5.0
 Compilation Date : May 25, 2022 06:01:34

 MPI Enabled;    Number of MPI Processes:       1
 OpenMP Disabled

 MPI version: 3.1
 MPI library version: Intel(R) MPI Library 2021.4 for Linux* OS

 Consult FDS Users Guide Chapter, Running FDS, for further instructions.
root@00a83c3c6390:/workdir#
```
