# `xfds  --help`
```
Usage: xfds [OPTIONS] COMMAND [ARGS]...

  Manage FDS simulations.

Options:
  -v, --version                   Display xFDS Version
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  run       Run an FDS simulation locally
  versions  List available FDS versions

  Developed by pbd.tools

```

# `xfds run --help`
```
Usage: xfds run [OPTIONS] [FDS_FILE]

  Run an FDS simulation locally

Arguments:
  [FDS_FILE]  The FDS file or directory to run. If a **FDS file** is specified,
              the FDS model will run. If a **directory** is specified, xFDS will
              find the first FDS file in the directory and assume that is what
              it should run. If no fds file exists, xFDS will default to
              interactive mode. if **nothing** is specified, the current
              directory is used and the above rules are applied.   [default: .]

Options:
  -i, --interactive               Launch Docker container in interactive mode
                                  (`docker run -it`). By default, the Docker
                                  image will run the FDS model, but interactive
                                  mode will put you into the container where you
                                  can start the FDS model manually. This is good
                                  for when you are rapidly iterating and don't
                                  want to wait for the Docker image load time.
  -n, --processors INTEGER RANGE  Specify number of processors. If the number of
                                  processors is greater than 1, it will invoke
                                  MPI for you (`mpiexec -n #`). Ignored if
                                  interactive mode is enabled.   [default: 1;
                                  x>=1]
  --fds TEXT                      Specify FDS version to use. The FDS version
                                  can also be extracted from the file path or
                                  metadata in the FDS file. Run `xfds versions`
                                  to see a list of available versions.
  --dry-run / --no-dry-run        View the command that would be run and exit.
                                  [default: no-dry-run]
  --help                          Show this message and exit.

  Developed by pbd.tools

```

# `xfds versions --help`
```
Usage: xfds versions [OPTIONS]

  List available FDS versions

Options:
  --help  Show this message and exit.

  Developed by pbd.tools

```