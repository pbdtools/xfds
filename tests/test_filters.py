from __future__ import annotations

import pytest

from xfds import _render as render

happy_tests = [
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
    ("{{ 100_000|str_convert('cfm', 'm^3/s', '%.2f')}}", "47.19"),
    # t2
    ("{{ 1000|t2(300) }}", "-300.0"),
    ("{{ 1600|t2(300)|round(2) }}", "-379.47"),
    # Supply/Exhaust
    ("{{ 10|supply }}", "-10"),
    ("{{ 10|exhaust }}", "10"),
    # IOR
    ("{{ 'x'|ior(from_target_to_device='+') }}", "1"),
    ("{{ 'x'|ior(from_target_to_device='-') }}", "-1"),
    ("{{ 'y'|ior(from_target_to_device='+') }}", "2"),
    ("{{ 'y'|ior(from_target_to_device='-') }}", "-2"),
    ("{{ 'z'|ior(from_target_to_device='+') }}", "3"),
    ("{{ 'z'|ior(from_target_to_device='-') }}", "-3"),
    ("{{ 'x'|ior(from_device_to_target='-') }}", "1"),
    ("{{ 'x'|ior(from_device_to_target='+') }}", "-1"),
    ("{{ 'y'|ior(from_device_to_target='-') }}", "2"),
    ("{{ 'y'|ior(from_device_to_target='+') }}", "-2"),
    ("{{ 'z'|ior(from_device_to_target='-') }}", "3"),
    ("{{ 'z'|ior(from_device_to_target='+') }}", "-3"),
]


sad_tests = [
    # xb
    "{{ (1, 2, 3, 4, 5)|xb }}",
    "{{ (1, 2, 3, 4, 5, 6, 7)|xb }}",
    # dxb
    "{{ (1, 2)|dxb(1, 1, 1) }}",
    "{{ (1, 2, 3, 4)|dxb(1, 1, 1) }}",
    # xyz
    "{{ (1, 2)|xyz }}",
    "{{ (1, 2, 3, 4)|xyz }}",
    # ijk
    "{{ (1, 2, 3, 4, 5)|ijk(0.1) }}",
    "{{ (1, 2, 3, 4, 5, 6, 7)|ijk(0.1) }}",
    # ior
    "{{ 'x'|ior() }}",
    "{{ 'i'|ior(from_device_to_target='-') }}",
    "{{ 'x'|ior(from_device_to_target='pbd') }}",
    "{{ 'i'|ior(from_target_to_device='-') }}",
    "{{ 'x'|ior(from_target_to_device='pbd') }}",
    # nodes
    "{{ 4|node(8) }}",
]


@pytest.mark.parametrize("tmpl, expected", happy_tests)
def test_happy_filters(tmpl: str, expected: str) -> None:
    assert render.compile(tmpl, {}) == expected


@pytest.mark.parametrize("tmpl", sad_tests)
def test_sad_filters(tmpl: str) -> None:
    with pytest.raises(ValueError):
        render.compile(tmpl, {})
