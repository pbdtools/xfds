!!! example
    All the input and output files on this page can be found in the [xFDS Examples directory](https://github.com/pbdtools/xfds/tree/main/examples).

xFDS allows you to add more features to your FDS input files using the [Jinja template syntax](https://jinja.palletsprojects.com/en/3.1.x/templates/). While this page will cover a high level overview of the Jinja syntax, the user is encouraged to read the Jinja documentation for more information.

xFDS uses Jinja's default delimeters. They are

- `{{ ... }}` indicates an **expression**. This can be a variable, calculation, or a function call.
- `{% ... %}` indicates a **statement** such as if/else conditionals and loops.
- `{# ... #}` indicates a **comment** and the contents of the block will be removed from the final fds file.

Normal FDS syntax is always valid, but you can use Jinja to help build your FDS lines.

## Defining Variables

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [variables](https://jinja.palletsprojects.com/en/3.1.x/templates/#variables)

The ability to set and use variables is what makes xFDS so powerful. There are three ways to define variables for your model.

### With Metadatain the FDS file

!!! Warning
    This method is intended for when you're only creating a single output model. If the project requires generating multiple scenarios from the FDS file, the [configuration file](./config.md) method should be used.

xFDS will read any metadata defined at the top of your file. The data must be at the very top of the FDS file and can optionally be enclosed by fences (`---`) above and below the data. After the metadata, there must be at least one single blank line to indicate the start of the content.

Metadata variables are case-insensitive and can contain letters, numbers, underscores, and dashes. They must be followed by a colon `:` and then the value. See the [Python Markdown Documentation](https://python-markdown.github.io/extensions/meta_data/#syntax) for more details.

**Without Fences**
```python title="examples/variables/variables.fds" linenums="1"
{! variables/variables.fds !}
```

**With Fences**
```python title="examples/fences/fences.fds" linenums="1"
{! fences/fences.fds !}
```

!!! Note
    `{{ value|int }}` uses the `int` filter to convert the value to an integer. See [filters](#filters) for more information.

xFDS will read the metadata and use the variables and use it to evaluate the expressions in the file. The variables for the `XB` parameter simply fill in the values while `IJK` will calculate the number of cells for each expression. This will generate the following output. Note that the metadata is carried through to the output file.

**Without Fences**
```python title="examples/variables/output/variables/variables.fds" linenums="1"
{! variables/output/variables/variables.fds !}
```
**With Fences**
```python title="examples/fences/output/fences/fences.fds" linenums="1"
{! fences/output/fences/fences.fds !}
```

!!! Note
    While this approach is not best suited for multiple files, it is a good idea to define metadata to help you understand the model later. You can even use Jinja expressions in defining the metadata. The `hrr` and `cfm` variables here would be defined in the configuration file. This would make the intent of the model clear without having to check the numbers manually.

    ```
    author: PBD Tools
    project: xFDS Documentation
    peak_hrr: {{ hrr }}
    exhaust: {{ cfm }}
    ```

### Using Jinja's Assignments

Jinja allows you to [assign](https://jinja.palletsprojects.com/en/3.1.x/templates/#assignments) values in the middle of your template. This can be useful when you want to perform a multi-step calculation or define a variable to use several times without having to define it. The variable may also be dynamic based on other inputs.

The following example automatically calculates the `HRRPUA` parameter and `XB` bounds for a 1000 kW fire on a 1.5 m<sup>2</sup> burner. Note how:

- **Line 9**: `top` is set so that the &VENT always sits on the top of the &OBST. Updating the variable will set the `zmin` and `zmax` for the &VENT as well as the `zmax` for the &OBST.
- **Line 10**: `area` is defined in the metadata, but the length of a `side` (for a square burner) is calculated in the template.
- **Line 11**: `r` (radius) is defined to be half the length of a side. This helps define the `XB` so the burner is perfectly centered regardless of the area.
- **Line 12**: `HRRPUA` is calculated based on the `hrr` and `area` variables defined. This way `HRRPUA` is always correct if either `hrr` or `area` are updated.
- **Lines 13-14**: The `XB` parameters use `r`, `top`, and `depth` to ensure the burner is centered and that the &VENT always aligns with &OBST.

```python title="examples/hrrpua/hrrpua.fds" linenums="1"
{! hrrpua/hrrpua.fds !}
```

```python title="examples/hrrpua/output/hrrpua/hrrpua.fds" linenums="1"
{! hrrpua/output/hrrpua/hrrpua.fds !}
```

**Variables can be set multiple times**

If a variable needs to take on different values for different parts of the model, the variable can be assigned a new value. Note how `top` is redefined on line 16 and lines 17-18 are the same as lines 13-14. This will change the `zmin` and `zmax` values for the second burner.

```python title="examples/hrrpua2/hrrpua2.fds" linenums="1"
{! hrrpua2/hrrpua2.fds !}
```

```python title="examples/hrrpua2/output/hrrpua2/hrrpua2.fds" linenums="1"
{! hrrpua2/output/hrrpua2/hrrpua2.fds !}
```

### In the Configuration File

When generating multiple output files from a single fds input file, a configuration file should be used. See [Configuration](./config.md) for more details.

## Control Structures

### If Statements

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [if statements](https://jinja.palletsprojects.com/en/3.1.x/templates/#if).

To make FDS records optional, use an `if` statement. The expression following the `if` keyword must evaluate to `True` or `False`. See this [Real Python article](https://realpython.com/python-boolean/) for more information on how Python evaluates truthiness.

In the example below, a varibale is defined for opening the mesh boundaries vs leaving them closed. Note how the only difference between the two files are the value of `bounds` on line 1. When the `bounds` are `closed`, the &VENT lines are omitted from the output file.

**Open Bounds**
```python title="examples/bounds_open/bounds_open.fds" linenums="1"
{! bounds_open/bounds_open.fds !}
```
```python title="examples/bounds_open/output/bounds_open/bounds_open.fds" linenums="1"
{! bounds_open/output/bounds_open/bounds_open.fds !}
```
**Closed Bounds**
```python title="examples/bounds_closed/bounds_closed.fds" linenums="1"
{! bounds_closed/bounds_closed.fds !}
```
```python title="examples/bounds_closed/output/bounds_closed/bounds_closed.fds" linenums="1"
{! bounds_closed/output/bounds_closed/bounds_closed.fds !}
```

If the model requires mutally exclusive options, `if`/`elif`/`else` blocks can be used.

```python
{% if ventillation == "natural" %}
    # open doors and windows
{% elif ventillation == "mechanical" %}
    # insert fans
{% else %}
    # room is sealed
{% endif %}
```

### For Loops

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [for loops](https://jinja.palletsprojects.com/en/3.1.x/templates/#for)

Sometimes it is beneficial to iterate through a list or quickly generate an array of items. While some FDS records can be duplicated with a &MULT record, this is not always the case.

Imagine needing to quickly layout a grid of sprinklers, and the sprinklers need to have unique names (e.g. for developing &CTRL records). Devices do not support &MULT records. For loops can assist in generating the sprinkler grid while calculating the position for each sprinkler individually.

By defining the number of sprinklers in each direction (`nx`, `ny`) and the sprinkler `spacing`, the location of the first sprinkler (`x_start`, `y_start`) is determined. Based on the initial sprinkler location and the spacing, the rest of the sprinkler positions are calculated and named based on the loop variables `i` and `j`.

```python title="examples/sprinkler_loop/sprinkler_loop.fds" linenums="1"
{! sprinkler_loop/sprinkler_loop.fds !}
```
!!! tip
    This example uses python's [printf-style formatting](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) along with the [format filter](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.format) to make the XYZ values line up.

    `%7.4f"|format(x)` tells xFDS how to format the value of `x`.

    - `%f`: format as a float
    - `%.4f`: format as a float to 4 decimals
    - `%7.4f`: format as float to 4 decimals and a fixed width of 7 characters (includes decimal '`.`' and sign '`-`')

Note how each sprinkler has a unique `ID` and the &MESH will adjust based on the number of sprinklers.

```python title="examples/sprinkler_loop/output/sprinkler_loop/sprinkler_loop.fds" linenums="1"
{! sprinkler_loop/output/sprinkler_loop/sprinkler_loop.fds !}
```

### Macros

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [macros](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros)

Macros are useful when defining complex elements that require multiple lines of FDS code or simple elements that are reused multiple times.

For example, defining a simple leakage path through a door requires at least three different FDS records, two &VENTs and one &HVAC. It may be beneficial to include an &OBST record to ensure the &VENT records are applied to a solid surface.

In the example below create doors along a wall in a corridor. A macro is defined on line 11 that takes in four parameters: the x position of the door, width and height of the door, and the leakage area. (The y position is fixed along the wall). The macro will determine the extends of the XB parameters and use a consistent naming scheme to tie the elements together.

!!! tip
    Macros can be called by passing in a list of values, or by specifying the parameter and value. Both options work the same, but specifying the parameter and value will make the file more readable.

    ```python linenums="38"
    {! leaks/leaks.fds [ln:38]!}
    ```
    ```python linenums="41"
    {! leaks/leaks.fds [ln:41]!}
    ```

Additionally, tenability devices are placed at 1 meter intervals along the corridor. A macro is defined on line 19 to ensure all the tenability criteria are defined at each location (visibility, temperature, O<sub>2</sub>, CO<sub>2</sub>, CO). The macro takes the x and y positions and will place all five devices at that location (the z position is hard coded in this example). A for loop (line 44) is used to set the 1 meter spacing starting at x = 1 m until the end of the corridor is reached.

```python title="examples/leaks/leaks.fds" linenums="1"
{! leaks/leaks.fds !}
```

```python title="examples/leaks/output/leaks/leaks.fds" linenums="1"
{! leaks/output/leaks/leaks.fds !}
```

!!! tip
    Use `namespace` to set up a counter that can be incremented to ensure unique IDs. Counters are initialized on line 9 as follows:

    ```python linenums="9"
    {! leaks/leaks.fds [ln:9]!}
    ```

    The following lines are located at the top of the respective macros and will increment the number by 1 every time the macro is called.

    ```python linenums="12"
    {! leaks/leaks.fds [ln:12]!}
    ```
    ```python linenums="20"
    {! leaks/leaks.fds [ln:20]!}
    ```

## Filters

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#filters).

Filters can modify the value of a variable or expression. This is useful when you need to ensure values follow a certain format. For example, in the &MESH lines above, IJK requires values to be integers. The `int` filter will ensure IJK gets integer values so FDS does not generate an error. The examples below demonstrate how to use some of the [built-in filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters) provided by Jinja.

### Absolute Value
```python title="examples/filters/filters.fds" linenums="2"
{! filters/filters.fds [ln:2] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="2"
{! filters/output/filters/filters.fds [ln:2] !}
```

### Center Text
```python title="examples/filters/filters.fds" linenums="5"
{! filters/filters.fds [ln:5] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="5"
{! filters/output/filters/filters.fds [ln:5] !}
```

### Convert to Float
```python title="examples/filters/filters.fds" linenums="8"
{! filters/filters.fds [ln:8-11] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="8"
{! filters/output/filters/filters.fds [ln:8-11] !}
```

### Convert to integer
```python title="examples/filters/filters.fds" linenums="14"
{! filters/filters.fds [ln:14-15] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="14"
{! filters/output/filters/filters.fds [ln:14-15] !}
```

### Maximum Value
```python title="examples/filters/filters.fds" linenums="18"
{! filters/filters.fds [ln:18] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="18"
{! filters/output/filters/filters.fds [ln:18] !}
```

### Minimum Value
```python title="examples/filters/filters.fds" linenums="21"
{! filters/filters.fds [ln:21] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="21"
{! filters/output/filters/filters.fds [ln:21] !}
```

### Round Value
```python title="examples/filters/filters.fds" linenums="24"
{! filters/filters.fds [ln:24] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="24"
{! filters/output/filters/filters.fds [ln:24] !}
```

### Trim Text
```python title="examples/filters/filters.fds" linenums="27"
{! filters/filters.fds [ln:27] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="27"
{! filters/output/filters/filters.fds [ln:27] !}
```

### Filter Unique Values
```python title="examples/filters/filters.fds" linenums="30"
{! filters/filters.fds [ln:30] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="30"
{! filters/output/filters/filters.fds [ln:30] !}
```

### Text to Uppercase
```python title="examples/filters/filters.fds" linenums="33"
{! filters/filters.fds [ln:33] !}
```
```python title="examples/filters/output/filters/filters.fds" linenums="33"
{! filters/output/filters/filters.fds [ln:33] !}
```
