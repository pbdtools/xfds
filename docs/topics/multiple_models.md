xFDS can generate multiple models from a single `pbd.yml` configuration file. Each item under the `render` parameter will be processed.

This is useful if when modeling drastically different sections of a building. For example, in modeling a large building such as an airport, the arrival terminal and gate areas may not need to be in the same simulation.

Another good use for this is to create small test cases. Three different models are defined in the example below:

- The primary model used for production
- A simple mesh resolution study
- A verification study to ensure the burner is working correctly.

!!! warning
    xFDS will always render EVERY model listed. Future versions will allow you to select which models to render.

!!! info
    See the [full example](https://github.com/pbdtools/xfds/tree/main/examples/multi_model) to see how the models are used and rendered.

```python title="examples/multi_model/pbd.yml" linenums="1"
{! multi_model/pbd.yml !}
```
