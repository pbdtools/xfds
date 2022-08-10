!!! note
    This page provides examples for how to write FDS files. However, all file listed under the `xfds.render.files` in the config file will have access to the template syntax described below.

!!! example
    All the input and output files on this page can be found in the [xFDS Examples directory](https://github.com/pbdtools/xfds/tree/main/examples).

xFDS allows you to add more features to your FDS input files using the [Jinja template syntax](https://jinja.palletsprojects.com/en/3.1.x/templates/). While this page covers a high level overview of the Jinja syntax, the user is encouraged to read the Jinja documentation for more information.

xFDS uses Jinja's default delimeters. They are:

- `{{ ... }}` indicates an **expression**. This can be a variable, calculation, or a function call.
- `{% ... %}` indicates a **statement** such as if/else conditionals and loops.
- `{# ... #}` indicates a **comment** and the contents of the block will be removed from the final fds file.

Normal FDS syntax is always valid, but you can use Jinja to help build your FDS lines.

## Defining Variables

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [variables](https://jinja.palletsprojects.com/en/3.1.x/templates/#variables)

The ability to set and use variables is what makes xFDS so powerful. There are two ways to define variables for your model.

### Using Jinja's Assignments

Jinja allows you to [assign](https://jinja.palletsprojects.com/en/3.1.x/templates/#assignments) values in the middle of your template. This can be useful when you want to use a value several times without having to type the value out each time. Variables also make it easy to keep things consistent. The variable may also be dynamic based on other inputs.

The following example automatically calculates the `HRRPUA` parameter and `XB` bounds for a 1000 kW fire on a 1.5 m<sup>2</sup> burner. Note how:

- **Line 9**: `top` is set so that the &VENT always sits on the top of the &OBST. Updating the variable will set the `zmin` and `zmax` for the &VENT as well as the `zmax` for the &OBST.
- **Line 10**: `area` is defined in at the top, but the length of a `side` (for a square burner) is calculated in the template.
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

To make FDS records optional, use an `if` statement. The expression following the `if` keyword must evaluate to `True` or `False`. See this [Real Python article](https://realpython.com/python-boolean/) for more information on how Python evaluates "truthiness".

In the example below, a varibale is defined for opening the mesh boundaries vs leaving them closed (default in FDS). Note how the only difference between the two files are the value of `bounds` on line 1. When the `bounds` are `closed`, the &VENT lines are omitted from the output file.

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

By defining the number of sprinklers in each direction (`nx`, `ny`) and the sprinkler `spacing`, the location of the sprinklers are determined. The [linspace](#linspace) filter will create `nx` sprinklers evenly spaced between `-dx / 2` and `dx / 2` and simlar for the y direction.

```python title="examples/sprinkler_loop/sprinkler_loop.fds" linenums="1"
{! sprinkler_loop/sprinkler_loop.fds !}
```

!!! tip
    When looping, it might be useful to know what loop iteration is being processed. The loop index can be accessed by `{{ loop.index }}`. This is used to set `i` and `j` for the device naming scheme above.

Note how each sprinkler has a unique `ID` and the &MESH will adjust based on the number of sprinklers. Additionally, the &OBST representing the burner is perfectly centered between the 4 central sprinklers!

```python title="examples/sprinkler_loop/output/sprinkler_loop/sprinkler_loop.fds" linenums="1"
{! sprinkler_loop/output/sprinkler_loop/sprinkler_loop.fds !}
```

### Macros

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [macros](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros)

Macros are useful when defining complex elements that require multiple lines of FDS code or simple elements that are reused multiple times.

For example, defining a simple leakage path through a door requires at least three different FDS records, two &VENTs and one &HVAC. It may be beneficial to include an &OBST record to ensure the &VENT records are applied to a solid surface.

The example below creates doors along a wall in a corridor. A macro is defined on line 11 that takes in four parameters: the x position of the door, width and height of the door, and the leakage area. (The y position is fixed along the wall). The macro will determine the extends of the XB parameters and use a consistent naming scheme to tie the elements together.

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

### Jinja Filters

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#filters).

Filters can modify the value of a variable or expression. This is useful when you need to ensure values follow a certain format or if a value needs to be modified. The examples below demonstrate how to use some of the [built-in filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters) provided by Jinja.

#### Absolute Value
```python title="examples/filters/abs.fds" linenums="1"
{! filters/abs.fds!}
```
```python title="examples/filters/output/filters/abs.fds" linenums="1"
{! filters/output/abs/abs.fds !}
```

#### Center Text
```python title="examples/filters/center.fds" linenums="1"
{! filters/center.fds !}
```
```python title="examples/filters/output/filters/center.fds" linenums="1"
{! filters/output/center/center.fds !}
```

#### Convert to Float

!!! tip
    In addition to the `float` filter, this example uses python's [printf-style formatting](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) along with the [format filter](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.format) to control the number of decimals displayed.

    `%7.4f"|format(x)` tells xFDS how to format the value of `x`.

    - `%f`: format as a float
    - `%.3f`: format as a float to 3 decimals
    - `%8.3f`: format as float to 3 decimals and a fixed width of 8 characters (includes decimal '`.`', sign '`-`', and extra white space at the beginning)

```python title="examples/filters/float.fds" linenums="1"
{! filters/float.fds !}
```
```python title="examples/filters/output/float/float.fds" linenums="1"
{! filters/output/float/float.fds !}
```

#### Convert to integer
```python title="examples/filters/int.fds" linenums="1"
{! filters/int.fds !}
```
```python title="examples/filters/output/int/int.fds" linenums="1"
{! filters/output/int/int.fds !}
```

#### Maximum Value
```python title="examples/filters/max.fds" linenums="1"
{! filters/max.fds !}
```
```python title="examples/filters/output/max/max.fds" linenums="1"
{! filters/output/max/max.fds !}
```

#### Minimum Value
```python title="examples/filters/min.fds" linenums="1"
{! filters/min.fds !}
```
```python title="examples/filters/output/min/min.fds" linenums="1"
{! filters/output/min/min.fds !}
```

#### Round Value
```python title="examples/filters/round.fds" linenums="1"
{! filters/round.fds !}
```
```python title="examples/filters/output/round/round.fds" linenums="1"
{! filters/output/round/round.fds !}
```

#### Trim Text
```python title="examples/filters/trim.fds" linenums="1"
{! filters/trim.fds !}
```
```python title="examples/filters/output/trim/trim.fds" linenums="1"
{! filters/output/trim/trim.fds !}
```

#### Filter Unique Values
```python title="examples/filters/unique.fds" linenums="1"
{! filters/unique.fds !}
```
```python title="examples/filters/output/unique/unique.fds" linenums="1"
{! filters/output/unique/unique.fds !}
```

#### Text to Uppercase
```python title="examples/filters/upper.fds" linenums="1"
{! filters/upper.fds !}
```
```python title="examples/filters/output/upper/upper.fds" linenums="1"
{! filters/output/upper/upper.fds !}
```

### xFDS Custom Filters

In addition to the built-in filters that comes with Jinja, xFDS ships with some additional filters useful for creating FDS records.

#### ARange

To create evenly spaced items, Python's [`range()` function](https://docs.python.org/3/library/functions.html#func-range) could be used, but it requires integer values for its parameters. [Numpy's `arange()` function](https://numpy.org/doc/stable/reference/generated/numpy.arange.html) allows floats to be used. xFDS defines this as a filter for convience.

```python title="examples/filters/arange.fds" linenums="1"
{! filters/arange.fds !}
```
```python title="examples/filters/output/arange/arange.fds" linenums="1"
{! filters/output/arange/arange.fds !}
```

#### Convert

Thanks to the magic of [pint](https://pint.readthedocs.io/en/stable/), xFDS will allow you to convert between units. You can define values in the config file with the desired units (determined by you) while ensuring that the correct units are passed to FDS. The `convert` will return a `float` type which could be used in further calculations. If the conversion will be part of the final output, the formatting can be controlled by using the `format` and `convert` filters together. Alternatively, `str_convert` can be used to improve readability.

!!! info
    - List of [supported units](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt) defined by pint.
    - List of [custom units](https://github.com/pbdtools/xfds/blob/main/src/xfds/units.py) defined by xFDS.

Pint allows [custom units](https://pint.readthedocs.io/en/stable/defining.html)
to be defined. xFDS will detect a file called `units.txt` located in the same directory as the configuration file. Here is a simple definition of a [smoot](https://en.wikipedia.org/wiki/Smoot).

```python title="examples/filters/units.txt" linenums="1"
{! filters/units.txt !}
```
```python title="examples/filters/convert.fds" linenums="1"
{! filters/convert.fds !}
```
```python title="examples/filters/output/convert/convert.fds" linenums="1"
{! filters/output/convert/convert.fds !}
```

#### DXB

Similar to the [`xb`](#xb) filter below, `dxb` takes a triplet representing the anchor point `(x, y, z)` and parameters to set the width, depth, and height respectfully. Specify `xloc`, `yloc`, or `zloc` as `min`, `max`, or `mid` to indicate how the anchor point should be treated. `dxb` also accepts a format string.

```python title="examples/filters/dxb.fds" linenums="1"
{! filters/dxb.fds !}
```
```python title="examples/filters/output/dxb/dxb.fds" linenums="1"
{! filters/output/dxb/dxb.fds !}
```

#### Exhaust/Supply

For a &VENT, the sign of either `VOLUME_FLOW` or `VELOCITY` defined on the &SURF indicates if the vent is a supply or exhaust. These filters take the value specified and ensure the sign is correct. This makes the intent of the surface type clear to the reader.

!!! Note
    In this example, the exhaust and supply are both calculated as positive values, but the filters ensure the signs are correct for the respective types.

```python title="examples/filters/exhaust.fds" linenums="1"
{! filters/exhaust.fds !}
```
```python title="examples/filters/output/exhaust/exhaust.fds" linenums="1"
{! filters/output/exhaust/exhaust.fds !}
```

#### IJK

The `ijk` filter will take an `xb` sextuplet along with a resolution to calculate the IJK values for a MESH. The way `ijk` converts a float to an integer can be controlled by passing in a `rouding` parameter.

- `rounding='ceil'`: Round the number up to the nearest integer.
- `rounding='round'`: Round the number to the nearest integer (default).
- `rounding='floor'`: Round the number down to the nearest integer.

```python title="examples/filters/ijk.fds" linenums="1"
{! filters/ijk.fds !}
```
```python title="examples/filters/output/ijk/ijk.fds" linenums="1"
{! filters/output/ijk/ijk.fds !}
```

#### IOR

For devices that measure surface properties, the user needs to tell FDS which way the device should point. The IOR property is defined as the direction from the target to the device. To ensure the direction is defined correctly, the `ior` filter takes the axis (`x`, `y`, or `z`) and either the direction `from_target_to_device` or `from_device_to_target` as `+` or `-`.

In the example below, the first device is located in the -X direction from the obstruction. Therefore, target is along the `x` axis and the direction can be defined either as either:

- `from_target_to_device="-"` (negative x direction)
- `from_device_to_target="+"` (positive x direction)

```python title="examples/filters/ior.fds" linenums="1"
{! filters/ior.fds !}
```
```python title="examples/filters/output/ior/ior.fds" linenums="1"
{! filters/output/ior/ior.fds !}
```

#### Linspace

[Numpy's `linspace()` function](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html) will generate evenly spaced intervals between two values. This is useful when records, such as DEVCs, need to be evenly spaced between two bounds such as tenability devices across a large space or a thermocouple tree.

```python title="examples/filters/linspace.fds" linenums="1"
{! filters/linspace.fds !}
```
```python title="examples/filters/output/linspace/linspace.fds" linenums="1"
{! filters/output/linspace/linspace.fds !}
```

#### t2

On a SURF, the TAU_Q parameter indicates the time at which the peak heat release rate is achieved. If a fire needs to be defined in terms of a standardized growth time (time to reach 1 MW), the `t2` filter will calculate TAU_Q from the peak heat release rate and characteristic growth time. Altenatively, alpha ($\alpha$) may be specified.

$$Q=1000*\left(\frac{t}{t_g}\right)^2=\alpha t^2$$

```python title="examples/filters/t2.fds" linenums="1"
{! filters/t2.fds !}
```
```python title="examples/filters/output/t2/t2.fds" linenums="1"
{! filters/output/t2/t2.fds !}
```

#### XB

The `xb` filter takes a list of six numbers `(x0, x1, y0, y1, z0, z1)` and formats the numbers to have a consistent format. A custom format string can be provided. See [Python's stringg formatting](https://docs.python.org/3/library/string.html#format-specification-mini-language) for more information.

```python title="examples/filters/xb.fds" linenums="1"
{! filters/xb.fds !}
```
```python title="examples/filters/output/xb/xb.fds" linenums="1"
{! filters/output/xb/xb.fds !}
```

#### XYZ

The `xyz` filter acts exactly the same as the `xb` filter, but takes a triplet rather than a sextuplet.

```python title="examples/filters/xyz.fds" linenums="1"
{! filters/xyz.fds !}
```
```python title="examples/filters/output/xyz/xyz.fds" linenums="1"
{! filters/output/xyz/xyz.fds !}
```

### User Defined Filters

!!! info "Jinja Docs"
    See the Jinja documentation for more information on [custom filters](https://jinja.palletsprojects.com/en/3.0.x/api/#custom-filters)

!!! Warning
    Custom functions that depend on packages that do not ship with xFDS might not work. If possible, stick to packages in the [Python standard library](https://docs.python.org/3/library/). Additionally, [Numpy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/) are included by default.

Users who are familiar with Python may create their own custom filters as desired. If there is a file called `filters.py` in the same directory as the configuration file `pbd.yml`, xFDS will import every function in `filters.py` and make it available to the template in `model.fds`.

See the [user_filters test case](https://github.com/pbdtools/xfds/tree/main/tests/test_render/user_filters) as an example or checkout the [xFDS custom filters source file](https://github.com/pbdtools/xfds/blob/main/src/xfds/filters.py).

```console title="/path/to/project/"
.
├── filters.py
├── model.fds
├── pbd.yml
└── units.txt
```
