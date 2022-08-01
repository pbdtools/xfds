from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent

import pytest
import yaml
from typer.testing import CliRunner

from xfds import _render as render
from xfds import errors
from xfds.cli import app

runner: CliRunner = CliRunner()


@pytest.fixture
def datadir_no_config(datadir: Path) -> Path:
    """Provides reference to no_config directory."""
    folder = datadir / "no_config"
    files = list(folder.iterdir())
    assert len(files) == 1
    assert files[0].stem != "pbd"
    return folder


@pytest.fixture
def datadir_no_fds(datadir: Path) -> Path:
    """Provides reference to no_config directory."""
    folder = datadir / "no_fds"
    files = list(folder.iterdir())
    assert len(files) == 1
    assert files[0].stem == "pbd"
    return folder


@pytest.fixture
def datadir_model(datadir: Path) -> Path:
    """Provides reference to no_config directory."""
    folder = datadir / "model"
    files = list(folder.iterdir())
    assert len(files) == 2
    return folder


@pytest.fixture
def datadir_filters(datadir: Path) -> Path:
    """Provides reference to no_config directory."""
    folder = datadir / "user_filters"
    return folder


########################################
# Unit Tests
########################################

# Happy Paths
def test_finds_config_file(datadir_no_fds: Path) -> None:
    config = render.locate_config(datadir_no_fds)
    assert config.stem == "pbd"


def test_config_loaded(datadir_model: Path) -> None:
    config_file = render.locate_config(datadir_model)
    config = render.read_config(config_file)
    assert "xfds" in config.keys()


def test_model_contains_variables_only_when_no_matrix() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model
          variables:
            pbd: tools
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 1
    assert scenarios[0]["data"] == {"pbd": "tools"}


def test_model_contains_matrix_and_default_variables() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model_{{pbd}}_{{tools}}
          variables:
            model: fds
            pbd: d
          parameters:
            pbd: [a, b, c]
            tools: [1, 2, 3]
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 9
    assert scenarios[0]["data"] == {"pbd": "a", "tools": 1, "model": "fds"}
    assert scenarios[-1]["data"] == {"pbd": "c", "tools": 3, "model": "fds"}


def test_adds_parameters_with_includes() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model_{{pbd}}_{{tools}}
          variables:
            model: fds
          parameters:
            pbd: [a, b, c]
            tools: [1, 2, 3]
            include:
              - pbd: a
                tools: 1
                bar: foo
              - pbd: c
                tools: 3
                foo: bar
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 9
    assert scenarios[0]["data"] == {
        "pbd": "a",
        "tools": 1,
        "model": "fds",
        "bar": "foo",
    }
    assert scenarios[-1]["data"] == {
        "pbd": "c",
        "tools": 3,
        "model": "fds",
        "foo": "bar",
    }
    assert len(scenarios[1]["data"]) == 3


def test_include_overrides_variable() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model_{{pbd}}_{{tools}}
          variables:
            tools: fds
          parameters:
            pbd: [a, b]
            include:
              - pbd: a
                tools: cfast
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 2
    assert scenarios[0]["data"] == {"pbd": "a", "tools": "cfast"}
    assert scenarios[1]["data"] == {"pbd": "b", "tools": "fds"}


def test_excludes() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model_{{pbd}}_{{tools}}
          variables:
            model: fds
          parameters:
            pbd: [a, b, c]
            tools: [1, 2, 3]
            exclude:
              - pbd: a
                tools: 1
              - pbd: b
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 5


def test_correct_filenames() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
          name: model_{{pbd}}_{{tools}}
          parameters:
            pbd: [a, b, c]
            tools: [1, 2]
            exclude:
              - pbd: b
    """
    config = yaml.safe_load(dedent(config_text))
    scenarios = render.parse_models(config)
    assert len(scenarios) == 4

    names = [
        "model_a_1",
        "model_a_2",
        "model_c_1",
        "model_c_2",
    ]
    assert names == [s["name"] for s in scenarios]


# Sad Paths
def test_raises_error_if_no_config(datadir_no_config: Path) -> None:
    with pytest.raises(errors.ConfigNotFound):
        render.locate_config(datadir_no_config)


def test_error_if_xfds_not_defined() -> None:
    config_text = """
    pbd: tools
    """
    config = yaml.safe_load(dedent(config_text))
    with pytest.raises(errors.xFDSNotDefined):
        render.parse_models(config)


def test_error_if_render_not_defined() -> None:
    config_text = """
    xfds:
      pbd: tools
    """
    config = yaml.safe_load(dedent(config_text))
    with pytest.raises(errors.RenderNotDefined):
        render.parse_models(config)


def test_error_if_name_not_specified() -> None:
    config_text = """
    xfds:
      render:
        - file: model.fds
    """
    config = yaml.safe_load(dedent(config_text))
    with pytest.raises(errors.ModelNameNotDefiend):
        render.parse_models(config)


def test_error_if_file_not_specified() -> None:
    config_text = """
    xfds:
      render:
        - name: pbdtools
    """
    config = yaml.safe_load(dedent(config_text))
    with pytest.raises(errors.InputFileNotDefined):
        render.parse_models(config)


########################################
# Integration Tests
########################################
@pytest.mark.integration_test
def test_render_help() -> None:
    """Ensure render function is available by calling for --help."""
    result = runner.invoke(app, ["render", "--help"])
    assert result.exit_code == 0


def test_loading_user_custom_filters(datadir_filters: Path) -> None:
    """Test that user defined filters can be loaded."""
    os.chdir(datadir_filters)
    output_file = datadir_filters / "output" / "model" / "model.fds"
    result = runner.invoke(app, ["render"])
    assert result.exit_code == 0
    assert output_file.read_text() == "Hello PBD Tools"


def gather_examples() -> list[Path]:
    examples_dir = Path(__file__).resolve().parents[1] / "examples"
    assert examples_dir.exists()
    examples = [config_file.parent for config_file in examples_dir.rglob("pbd.yml")]
    return examples


@pytest.mark.parametrize("directory", gather_examples())
def test_example_renders(directory: Path) -> None:
    print(directory)
    result = runner.invoke(app, ["render", str(directory)])
    assert result.exit_code == 0
