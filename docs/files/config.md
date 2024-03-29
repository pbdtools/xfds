!!! info
    For users who are not faimilar with yaml, [learnxinyminutes.com](https://learnxinyminutes.com/docs/yaml/) provides a good way to learn yaml pretty quickly.

The configuration file is a yaml file that tells xfds how you want things to work. It should be located at the top directory for your modeling project.

xFDS will look for the configuration file, `pbd.yml` when it is called (`pbd.yaml` is also acceptable). All configurations for xFDS start with the `xfds` keyword followed by the xFDS command and it's options.

```yaml title="/path/to/project/pbd.yml"
xfds:
  render:
    # render command options
    ...
  reset:
    # reset command options
    ...
  run:
    # run command options
    ...
```

## Render

The `xfds render` command takes a list of objects that define the model and associated data. Each object takes the following parameters:

- **name**: The name to be used for naming the output files. The name should contain placeholders for variables to ensure unique file names. The file extension for the output files is taken from the given input file.
- **files**: Names of the input files to be included in the output directory. The input files are templates used for each scenarios.
- **variables**: A list of default variables to send to the fds template while rendering the output files. These variables are not considered in generating scenarios.
- **parameters**: Variables defined in the parameters section will tell xFDS which parameters to use in generating scenarios. All variables defined here should have a list of values to consider.
    - **include**: Directive defining extra information to add to scenarios.
    - **exclude**: Directive defining conditions for removing scenarios.

!!! warning
    The `name` parameter must start with a letter
    ```yaml
    xfds:
      render:
        - name: 2-way-flow # This is invalid
          files:
            - input.fds
        - name: two-way-flow # This works
          files:
            - input.fds
    ```

The example below shows a configuration for a mesh sensitivity study. This assumes there is a file `sensitivity.fds` in the same directory and that the file looks for two variables, `hrr` and `resolution`. Running `xfds render` will generate three output files:

* sensitivity_10cm.fds
* sensitivity_15cm.fds
* sensitivity_20cm.fds

```yaml title="pbd.yml"
xfds:
  render:
    - name: sensitivity_{{resolution * 100}}cm
      files:
        - sensitivity.fds
      variables:
        hrr: 1000
      parameters:
        resolution: [0.10, 0.15, 0.20]
```

### Parameters

All parameters defined under the `parameters` option are used to generate the different scenarios. The input below will generate a series of models. The `include` and `exclude` directives will modify the scenarios as described below.

```yaml title="examples/simple_atrium/pbd.yml"
xfds:
  render:
    - name: atrium_{{cfm}}_{{mua_perc}}
      files:
        - simple_atrium.fds
      variables:
        ...
      parameters:
        cfm: [100_000, 125_000, 150_000]  # cfm
        mua_perc: [0, 85, 90, 95] # %
        include:
            # Open doors if makeup air percentage is 0
          - mua_perc: 0
            open_doors: true
        exclude:
            # Not enough duct area to supply > 90% of cfm
          - cfm: 150_000
            mua_perc: 95
          - cfm: 150_000
            mua_perc: 90
```

Twelve scenarios were generated. There are 3 values for `cfm` and 4 values for `mua_perc`. Every combination of values are listed below.

```python title="Initial Scenarios"
{ cfm: 100_000, mua_perc: 0 }
{ cfm: 100_000, mua_perc: 85 }
{ cfm: 100_000, mua_perc: 90 }
{ cfm: 100_000, mua_perc: 95 }
{ cfm: 125_000, mua_perc: 0 }
{ cfm: 125_000, mua_perc: 85 }
{ cfm: 125_000, mua_perc: 90 }
{ cfm: 125_000, mua_perc: 95 }
{ cfm: 150_000, mua_perc: 0 }
{ cfm: 150_000, mua_perc: 85 }
{ cfm: 150_000, mua_perc: 90 }
{ cfm: 150_000, mua_perc: 95 }
```

!!! warning
    Each parameter must have a value that is iterable (a list of values).

    ```yaml title="pbd.yml"
    parameters:
      single_line: [1, 2, 3]
      multile_line:
        - 1
        - 2
        - 3
      single_value_iterable: [42] # lists can have a single value
    ```

    These will not work

    ```yaml title="pbd.yml"
    parameters:
      single_value_not_iterable: 42 # scalar value must be in a list
      parenthesis_are_not_valid: (1, 2, 3) # syntax error
    ```

#### Include directive

The `include` directive will update the models in the order they are defined. xFDS will determine which keys in the directive match parameters already defined. If the values of the keys match the parameters, the additional records in the directive will be appended to the scenario. In this example, we have a directive that says "any scenario where the makeup air percentage is 0%, add `open_doors = true`"

```python title="Scenarios after Include"
{ cfm: 100_000, mua_perc: 0, open_doors: True }
{ cfm: 100_000, mua_perc: 85 }
{ cfm: 100_000, mua_perc: 90 }
{ cfm: 100_000, mua_perc: 95 }
{ cfm: 125_000, mua_perc: 0, open_doors: True }
{ cfm: 125_000, mua_perc: 85 }
{ cfm: 125_000, mua_perc: 90 }
{ cfm: 125_000, mua_perc: 95 }
{ cfm: 150_000, mua_perc: 0, open_doors: True }
{ cfm: 150_000, mua_perc: 85 }
{ cfm: 150_000, mua_perc: 90 }
{ cfm: 150_000, mua_perc: 95 }
```

#### Exclude Directive

The `exclude` directive will eliminate scenarios matching each directive given. In this example, the configuration file is stating "for an exhaust rate of 150,000 cfm, there is not enough mechanical makeup air supply to reach >= 90% of the flow." These scenarios are removed accordingly.

```python title="Scenarios after Exclude"
{ cfm: 100_000, mua_perc: 0, open_doors: True }
{ cfm: 100_000, mua_perc: 85 }
{ cfm: 100_000, mua_perc: 90 }
{ cfm: 100_000, mua_perc: 95 }
{ cfm: 125_000, mua_perc: 0, open_doors: True }
{ cfm: 125_000, mua_perc: 85 }
{ cfm: 125_000, mua_perc: 90 }
{ cfm: 125_000, mua_perc: 95 }
{ cfm: 150_000, mua_perc: 0, open_doors: True }
{ cfm: 150_000, mua_perc: 85 }
```

In the end, 10 scenarios remain and xFDS will generate 10 models.

## Reset

When testing out changes in models, it is sometimes useful to remove the old output files. The `xfds reset` command will delete all files in the directory unless they match a specified pattern.

To keep certain files when `xfds reset` is run, specify the file patterns with the `keep` parameter. Use [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming)) to specify which files you want to keep.

```yaml title="pbd.yml"
xfds:
  reset:
    keep:
      - '*.fds'
      - '*.ini'
      - '*.in'
      - '*.zip'
```

## Run

Configuration options are not available at this time. See the [run command](/commands/run) for more information
