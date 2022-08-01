from __future__ import annotations

import pytest

from xfds import _render as render

tests = [
    # xb filter
    (
        "{{ (-2, 2, -1, 1, 0, 3)|xb }}",
        " -2.000,  2.000, -1.000,  1.000,  0.000,  3.000",
    ),
    (
        "{{ (-2, 2, -1, 1, 0, 3)|xb('%6.2f') }}",
        " -2.00,  2.00, -1.00,  1.00,  0.00,  3.00",
    ),
    # ijk
    ("{{ (0, 5, 0, 4, 0, 3)|ijk(0.1) }}", "50,40,30"),
    ("{{ (0, 5, 0, 4, 0, 3)|ijk(0.2) }}", "25,20,15"),
    ("{{ (0, 5, 0, 4, 0, 3)|ijk(0.3) }}", "17,13,10"),
    ("{{ (0, 5, 0, 4, 0, 3)|ijk(0.3, 'ceil') }}", "17,14,10"),
    ("{{ (0, 5, 0, 4, 0, 3)|ijk(0.3, 'floor') }}", "16,13,10"),
    # dxb
    (
        "{{ (0, 0, 0)|dxb(3, 2, 1) }}",
        " -1.500,  1.500, -1.000,  1.000, -0.500,  0.500",
    ),
    (
        "{{ (0, 0, 0)|dxb(3, 2, 1, zloc='min') }}",
        " -1.500,  1.500, -1.000,  1.000,  0.000,  1.000",
    ),
    (
        "{{ (0, 0, 0)|dxb(3, 2, 1, zloc='max') }}",
        " -1.500,  1.500, -1.000,  1.000, -1.000,  0.000",
    ),
    # xyz
    (
        "{{ (1, 2, 3)|xyz }}",
        "  1.000,  2.000,  3.000",
    ),
    (
        "{{ (1, 2 , 3)|xyz('%6.2f') }}",
        "  1.00,  2.00,  3.00",
    ),
    # convert
    (
        "{{ 212|convert('degF', 'degC')|round }}",
        "100.0",
    ),
    (
        "{{ (1, 2 , 3)|xyz('%6.2f') }}",
        "  1.00,  2.00,  3.00",
    ),
    ("{{ 100_000|str_convert('cfm', 'm^3/s', '%.2f')}}", "47.19"),
]


@pytest.mark.parametrize("tmpl, expected", tests)
def test_convert(tmpl: str, expected: str) -> None:
    assert render.compile(tmpl, {}) == expected