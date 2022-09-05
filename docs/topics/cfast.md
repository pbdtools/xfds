Despite its name, xFDS can render any text file as a template. It can handle CFAST files just as easily as FDS or PBS files.

Defining a fire in the CFAST editor can be tedious, especially if the area or product yields need to be altered over time. With xFDS, these parameters can be programatically set. The example below shows how the fire can easily be changed from a medium growth (tg = 300 s) to a slow growth (tg = 600 s) fire.

!!! tip
    If a project requires both CFAST and FDS models, they can be managed from the same `pbd.yml` configuration file!

```python title="examples/cfast/pbd.yml" linenums="1"
{! cfast/pbd.yml !}
```

```python title="examples/cfast/cfast.in" linenums="1"
{! cfast/cfast.in !}
```

!!! note
    This model uses a custom filter to get the heat release rate as a function of time

```python title="examples/cfast/filters.py" linenums="1"
{! cfast/filters.py !}
```

```python title="examples/cfast/output/t2-fire_tg-300s/t2-fire_tg-300s.in" linenums="1"
{! cfast/output/t2-fire_tg-300s/t2-fire_tg-300s.in !}
```

```python title="examples/cfast/output/t2-fire_tg-600s/t2-fire_tg-600s.in" linenums="1"
{! cfast/output/t2-fire_tg-600s/t2-fire_tg-600s.in !}
```
