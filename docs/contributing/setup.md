## Setting up for Development

You can work from anywhere on your system, however, these instructions assume you're on a unix operating system, have the username `pbdtools` and the code will be located at `/home/pbdtools/xfds/`.

### Install xFDS required software

Refer to the [xFDS installation instructions](../installation.md)

### Install Git

!!!info
    [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

Install [Git](https://git-scm.com/downloads) on your machine. Git is used for version control and must be used to contribute to the code base.

Once you have Git installed, follow the [first time Git setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) instructions.

```console title="/home/pbdtools"
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
```

### Fork and Clone the Repository

Go to the [project repository](https://github.com/pbdtools/xfds) and in the top right of the page, click "fork" to make a fork of the repository in your account.

Navigate to where you want to copy the files and clone your fork of the repository. Make sure to change `<USERNAME>` to your Github user name.

```console title="/home/pbdtools/"
git clone https://github.com/<USERNAME>/xfds.git
cd xfds
```

### Install Poetry

!!!info
    [Installing Poetry](https://python-poetry.org/docs/#installation)

[Poetry](https://python-poetry.org) is used to manage dependencies and build xFDS for distribution. Follow their [installation instructions](https://python-poetry.org/docs/#installation) for your operating system.

Once Python and Poetry are installed, you can install the required packages with the [`poetry install`](https://python-poetry.org/docs/cli/#install) command.

```console title="/home/pbdtools/xfds/"
poetry install
```

## Setting up for Testing

### Install Nox

[Nox](https://nox.thea.codes/en/stable/) is used to test xFDS on different versions of Python. A whole suite of tests are defined in [`noxfile.py`](https://github.com/pbdtools/xfds/blob/main/noxfile.py)

The Nox documentation suggests installing nox with `pip`, but `pipx` will isolate Nox from any other dependencies

=== "pipx"
    ```console title="/home/pbdtools/"
    pipx install nox
    ```
=== "pip"
    ```console title="/home/pbdtools/"
    pip install --user --upgrade nox
    ```

## Other Tools

### Just

!!!info
    [Installing Just](https://github.com/casey/just#installation)

[Just](https://github.com/casey/just) provides a way to save and run project-specific commands. These commands are stored in the [`justfile`](https://github.com/pbdtools/xfds/blob/main/justfile). Follow their [installation instructions](https://github.com/casey/just#installation) for your operating system.

Below are some example commands and their equivalents.

**Install Project Dependencies**
=== "just"
    ```console title="/home/pbdtools/xfds"
    just install
    ```
=== "poetry"
    ```console title="/home/pbdtools/xfds"
    poetry install
    ```

**Run pre-commit on All Files**
=== "just"
    ```console title="/home/pbdtools/xfds"
    just check
    ```
=== "poetry"
    ```console title="/home/pbdtools/xfds"
    poetry run pre-commit run --all-files
    ```

**Run pytest Suite on All Versions of Python**
=== "just"
    ```console title="/home/pbdtools/xfds"
    just tests
    ```
=== "nox"
    ```console title="/home/pbdtools/xfds"
    nox -rs tests
    ```

**Install Current Development Version with pipx**

=== "just"
    ```console title="/home/pbdtools/xfds"
    just pipx
    ```
=== "pipx"
    ```console title="/home/pbdtools/xfds"
    rm -Rf dist
    poetry build
    pipx install --force `find ./dist -name "*.whl" | sort | tail -n 1`
    ```

**View Documentation**
=== "just"
    ```console title="/home/pbdtools/xfds"
    just docs
    ```
=== "poetry"
    ```console title="/home/pbdtools/xfds"
    poetry run mkdocs serve
    ```
