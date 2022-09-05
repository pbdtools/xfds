# Stop Command

## Usage
```txt title="xfds stop --help"
{! ../docs/commands/stop.help.txt !}
```

## Description

The `stop` command creates a `casename.stop` file in the model directory telling FDS to gracefully terminate.

If a FDS file is passed, xFDS will create a `.stop` file for that specific FDS file. Otherwise, xFDS will locate all FDS files in the directory and create `.stop` files for them. This is especially handy when `&CATF` is used and the actual model is `casename_cat.fds`.

These two snippets are effecively the same.

```sh title="/path/to/model (With xFDS)"
xfds stop
```

```sh title="/path/to/model (Without xFDS)"
for f in *.fds; do touch "$f" "${f%.fds}.stop"; done
```
