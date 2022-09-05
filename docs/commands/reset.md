# Reset Command

## Usage
```txt title="xfds reset --help"
{! ../docs/commands/reset.help.txt !}
```

## Description

The `reset` command will reset the fire model direcory so that it only contains the desired files, generally the input files. A few examples where this may be useful are as follows:

- Reset the directory so only the input files remain. This way, when a model is run again, there is a high level of confidence that every file in the directory correlates to the given model.
- Remove bulky output files. Depending on the analysis, it may not be necessary to keep the large binary files. After backing up the models to a server, disk space can be saved by deleting the files necessary for Smokeview.
- When processing models, there might be extra files generated, such as exporting images from Smokeview. A pattern could be used to ensure all the model outputs remain, but the extra files are removed.

xFDS uses the [glob syntax](https://en.wikipedia.org/wiki/Glob_(programming)) to denote which files to keep. See the [config file](/files/config/#reset) for more information.

```python title="tests/test_reset/model/pbd.yml" linenums="1"
{! ../tests/test_reset/model/pbd.yml !}
```
