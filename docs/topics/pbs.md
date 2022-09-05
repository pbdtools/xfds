## xFDS can programmatically generate `.pbs` files!

If you need [`.pbs` files](https://en.wikipedia.org/wiki/Portable_Batch_System), simply add the `.pbs` file to the `files` parameter in the [config file](/files/config/#render) and build your `.pbs` file as you would any other [template](/files/input).

In the simple atrium example, a variable `proc` is defined to indicate the number of processors required and is accessable in the template.

In Python, `//` is the operator for floor division. Therefore, `{{ proc // <ppn> }}` will produce the number of full nodes required. For example, if the model requires 28 nodes and each node has 8 processors, `{{ proc // 8 }}` will render as `3` implying that 3 full nodes are required.

In Python, `%` is the operator for determining the remainder. Therefore `{{ proc % <ppn> }}` will produce the number of cores needed on a partial node. For example, if the model requires 28 nodes and each node has 8 processors, `{{ proc % 8 }}` will render as `4` implying only 4 cores are required on that node.

```python title="examples/simple_atrium/pbd.yml" linenums="1"
{! simple_atrium/pbd.yml [ln:1-8] !}
...
```

```python title="examples/simple_atrium/simple_atrium.pbs" linenums="1"
{! simple_atrium/simple_atrium.pbs !}
```

!!! tip
    Use the [`xfds.render.parameters.include` directive](/files/config/#include-directive) if you need to modify the number of processors based on the a specific configuration.

If you require fewer cores than available on a single node, `{{ n // 8 }}` will render to `0`. Similarly, if the number of required cores is a multiple of the cores on a single node, `{{ n % 8 }}` will render to `0`. If this is undesireable, use an if statement containing the `node` filter.

The `node` filter requires two parameters in addition to the number of cores needed: ppn, or how many processors there are per node, and what mode to consider. The modes are as follows:

- `full`: Returns `True` if at least one full node is required.
- `part`: Returns `True` if a partial node is required.
- `both`: Returns `True` if both `full` and `part` are required.

!!! tip
    Use [Jinja's whitespace control syntax](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control) to collapse multiple lines onto one line.

```python title="examples/pbs/pbd.yml" linenums="1"
{! pbs/pbd.yml !}
```

```python title="examples/pbs/model.pbs" linenums="1"
{! pbs/model.pbs !}
```

If only 4 of the 8 processors on a node are needed, only 4 are requested.
```python title="examples/pbs/output/using_4_nodes/using_4_nodes.pbs" linenums="1"
{! pbs/output/using_4_nodes/using_4_nodes.pbs !}
```
If all 8 of the 8 processors on a node are needed, all 8 are requested.
```python title="examples/pbs/output/using_8_nodes/using_8_nodes.pbs" linenums="1"
{! pbs/output/using_8_nodes/using_8_nodes.pbs !}
```
If 12 processors are needed, but there are only 8 processors on a node, a full node of 8 processors and a partial node of 4 processors are requested.

```python title="examples/pbs/output/using_12_nodes/using_12_nodes.pbs" linenums="1"
{! pbs/output/using_12_nodes/using_12_nodes.pbs !}
```
