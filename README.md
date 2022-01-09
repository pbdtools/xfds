# xFDS

Tool for managing FDS runs with [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles).

- `docker`
- `run`
- `--rm` (Clean up after exit)
- `--it` (interactive)
- `-v`
  - `$(pwd)` (Linux / Mac)
  - `${pwd}` (PowerShell)
  - `%cd%` (Command Prompt)
- `:`
  - `/workdir` (Linux Container)
  - `C:\workdir` (Windows Container)
- `openbcl/fds` (defaults to latest if version not specified)
  - `:6.7.7`
  - `:6.7.6`
  - ...
- `mpiexec -n <meshcount>` (optional)
- `fds`
- `<filename>.fds`

## Dependencies
- [typer](https://typer.tiangolo.com/)
