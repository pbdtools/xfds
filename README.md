

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

Do you have [FDS](https://github.com/firemodels/fds) installed on your machine? Do you know where the FDS executable is located? Do you know what version it is? Maybe you have multiple versions of FDS on your machine, but do you know which one do you use?

Perhaps you generate a large number of spreadsheets to help you generate fire models. Are you tired of copying and pasting data all over the place? Do you spend a lot of time debugging your FDS code because that fire is just a bit off it's mark? 🤯

Designed to save you time, xFDS is meant to help generate and manage your fire models. Sound too good to be true? **Learn more at [xfds.pbd.tools](https://xfds.pbd.tools)**! 🤓

Not quite convinced it's worth it? Watch the presentation from [FEMTC 2022](https://www.femtc.com/events/2022/d1-09-cohan/) or let us tell you more...

## Features

### Generate Parametric Analyses

Fire models can often require mesh sensitivity studies, different fire sizes, adjusting exhaust rates, or messing with a number of differnt parameters. With the power of the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) templating system, xFDS can help generate and fine tune a variety of models from a single `.fds` file!

#### Specify Resolution, not `IJK`

Let xFDS calculate the number of cells so you don't have to. By setting variables in your [FDS file](https://xfds.pbd.tools/files/input/) or [configuration file](https://xfds.pbd.tools/files/config/), you can use them to perform calculations. Anything between double curly braces `{{` and `}}` is evaluated as [Python](https://www.python.org/) code.

```python title="Meet your new input file."
{% set xmax, ymax, zmax = 5, 4, 3 %}
{% set res = 0.2 %}
&MESH XB=0, {{ xmax }}, 0, {{ ymax }}, 0, {{ zmax }},
      IJK={{ xmax // res }}, {{ ymax // res }}, {{ zmax // res }}/
```

Will translate to:

```python title="A nicely formatted &MESH line!"
&MESH XB= 0, 5, 0, 4, 0, 3,
      IJK= 25, 20, 15/
```

Want to run a finer mesh? Just change `res` to `0.1` and get

```python title="One mighty fine &MESH!"
&MESH XB= 0, 5, 0, 4, 0, 3,
      IJK= 50, 40, 30/
```

Feel like that template is a bit verbose? xFDS has some convience [template filters](https://xfds.pbd.tools/files/input/#filters) to make your life easier.

```python title="Filters make your code easier to read."
{% set bounds = 0, 5, 0, 4, 0, 3 %}
&MESH XB={{ bounds|xb }}, IJK={{ bounds|ijk(res) }}
```

#### Don't think, KNOW your HRRPUA is correct

It can be tricky to tell if the Heat Release Rate Per Unit Area (HRRPUA) parameter is correct. Are you sure the area used for the burner will give you the correct heat release rate (HRR)? With xFDS, you can define your `HRR` and `Area` then let xFDS do the calculations for you! 🚀

```python title="Let xFDS do the hard part"
{% set hrr = 1000 %}
{% set area = 1.5 %}

{% set offset = (area ** 0.5) / 2 %}
&SURF ID='BURNER', COLOR='RED', HRRPUA={{ (hrr / area)|round(2) }}/
&VENT XB={{ (-offset, offset, -offset, offset, 0.0, 0.0)|xb }}, SURF_ID='BURNER'/
```

Go ahead and try out this burner and see if xFDS got it right. 😉

```Python title="We added a few lines to help you out"
&MESH XB=-2, 2, -2, 2, 0, 4, IJK=60, 60, 60/
&TIME T_END=10/
&REAC FUEL='PROPANE'/

---
&SURF ID='BURNER', COLOR='RED', HRRPUA=666.67/
&VENT XB= -0.612,  0.612, -0.612,  0.612,  0.000,  0.000, SURF_ID='BURNER'/
---

&VENT MB='XMIN', SURF_ID='OPEN'/
&VENT MB='XMAX', SURF_ID='OPEN'/
&VENT MB='YMIN', SURF_ID='OPEN'/
&VENT MB='YMAX', SURF_ID='OPEN'/
```

#### Use loops to create an array of devices

Tired of generating a bunch of items? Use [for loops](https://xfds.pbd.tools/files/input/#for-loops) to get it done faster!

Here, xFDS creates 8 thermocouples evenly spaced between 1 ft and 8 ft. Yep, you can specify things in whatever unit you want thanks to the [convert filter](https://xfds.pbd.tools/files/input/#convert)

```python title="You'll be doing loops around your competition!"
{% set n_thcps, bottom, top = 8, 1|convert('ft', 'm'), 8|convert('ft', 'm') %}
{% for z in n_thcps|linspace(bottom, top) %}
&DEVC ID="THCP_{{ loop.index }}" QUANTITY='THERMOCOUPLE', XYZ={{ (0, 0, z)|xyz }}/
{% endfor %}
```

Will render to the following code.

```python title="Look at that number for"
&DEVC ID="THCP_1" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  0.305/
&DEVC ID="THCP_2" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  0.610/
&DEVC ID="THCP_3" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  0.914/
&DEVC ID="THCP_4" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  1.219/
&DEVC ID="THCP_5" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  1.524/
&DEVC ID="THCP_6" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  1.829/
&DEVC ID="THCP_7" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  2.134/
&DEVC ID="THCP_8" QUANTITY='THERMOCOUPLE', XYZ=  0.000,  0.000,  2.438/
```

### Manage FDS Runs

#### Auto-detect FDS file in directory

If you're in a directory containing an FDS file, xFDS will find the FDS file without you specifying it. All you need to do is say [`xfds run`](http://xfds.pbd.tools/commands/run/)!

#### Latest version of FDS always available.

xFDS will always default to the latest version thanks to how the Docker images are created. You can always use an older version of FDS if needed and xFDS makes it easy to work with any version of FDS you need.

#### Always know what FDS version you're using.

xFDS will inject the FDS version into the Docker container name so there's no question what version of FDS is running.

#### Runs in Background

Fire and forget. xFDS will run your model in a Docker container and free up your terminal for you to keep working.
