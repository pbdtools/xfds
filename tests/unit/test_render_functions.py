from textwrap import dedent
from typing import Union

import pytest

import xfds._render as render


@pytest.mark.parametrize(
    "input,output", [("42", 42), ("3.14", 3.14), ("pbd", "pbd"), ("", "")]
)
def test_normalize(input: str, output: Union[int, float, str]) -> None:
    assert render._normalize(input) == output


def test_meta() -> None:
    file_contents = dedent(
        """
    title: My Title
    value: 3.14
    resolutions: 1
                 2
                 3
    authors: me
             myself
             I

    &MESH /
    """
    ).lstrip()

    expected = {
        "title": "My Title",
        "value": 3.14,
        "resolutions": [1, 2, 3],
        "authors": ["me", "myself", "I"],
    }

    meta = render.get_meta(file_contents)
    assert meta == expected
