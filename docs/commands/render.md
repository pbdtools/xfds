# Render Command

## Usage
```txt title="xfds render --help"
{! ../docs/commands/render.help.txt !}
```

## Description

The xFDS render command converts template input files into usable modeling files. From a given directory (or the current directory if not specified), xFDS will traverse up the file system until it finds a `pbd.yml` [configuration file](/files/config/). It then parses the contents of the configuration file and generates a model for each set of [parameters](/files/config/#parameters).

Each input file specified in the configuration file will be treated like a [template](/files/input/). The templates will be processed with the data specified in the configuration file and placed in an `output` directory.

For example, the configuration file below expects two files to be located in the same directory as the configuration file: `model.fds` and `model.pbs`. It recognizes that a single `parameter` is set.

```python title="examples/pbs/pbd.yml" linenums="1"
{! pbs/pbd.yml !}
```

The two input files are defined in a way that uses the `n` parameter from the configuration file. The `model.fds` template is a simple file that just creates `n` meshes placed next to each other in the x-direction. Meahwhile, the `model.pbs` template is a partial PBS file showing how the nodes specifications can be altered based on the `n`umber of processors required (assuming 1 processor per mesh).

```python title="examples/pbs/model.fds" linenums="1"
{! pbs/model.fds !}
```
```python title="examples/pbs/model.pbs" linenums="1"
{! pbs/model.pbs !}
```

xFDS will process each of the templates and place them in a directory `./output/using_{{n}}_nodes` where `{{n}}` is replaced by the parameter `n`. Each model is placed in its own directory where the name matches the input files.

!!! tip
    While xFDS will treat every specified file as a template, if there is no template syntax defined, the file will be copied over to the output directory and be given the same base name as the model file. This is useful for having consistent Smokeview scripts, Smokeview ini files, or other files for each model.

!!! warning
    xFDS will use the `name` defined in the configuration file and match the file extension from the template file. This is how `model.fds` gets renamed to `using_{{n}}_nodes.fds` in the output.

    If you are using the `&CATF` feature in FDS, make sure the `OTHER_FILES` do not have an `.fds` file extension. Use a `.txt` or `.data` extension instead if you need to use this feature.

    You can have multiple `.fds` files in a project as long as they're specified as [different models](/topics/multiple_models/).

Files in `output/using_4_nodes`:
```python title="examples/pbs/output/using_4_nodes/using_4_nodes.fds" linenums="1"
{! pbs/output/using_4_nodes/using_4_nodes.fds !}
```
```python title="examples/pbs/output/using_4_nodes/using_4_nodes.pbs" linenums="1"
{! pbs/output/using_4_nodes/using_4_nodes.pbs !}
```

Files in `output/using_8_nodes`:
```python title="examples/pbs/output/using_8_nodes/using_8_nodes.fds" linenums="1"
{! pbs/output/using_8_nodes/using_8_nodes.fds !}
```
```python title="examples/pbs/output/using_8_nodes/using_8_nodes.pbs" linenums="1"
{! pbs/output/using_8_nodes/using_8_nodes.pbs !}
```

Files in `output/using_12_nodes`:
```python title="examples/pbs/output/using_12_nodes/using_12_nodes.fds" linenums="1"
{! pbs/output/using_12_nodes/using_12_nodes.fds !}
```
```python title="examples/pbs/output/using_12_nodes/using_12_nodes.pbs" linenums="1"
{! pbs/output/using_12_nodes/using_12_nodes.pbs !}
```
