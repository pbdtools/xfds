from __future__ import annotations

import math

FLOAT_FORMAT: str = "%7.3f"


def xb(values: list[float], fmt: str = FLOAT_FORMAT) -> str:
    """Format values for XB parameter."""
    if len(values) != 6:
        raise ValueError(f"XB must have 6 values, got {values}")

    return ",".join([fmt % v for v in values])


def dxb(
    xyz: list[float],
    dx: float,
    dy: float,
    dz: float,
    xloc: str = "mid",
    yloc: str = "mid",
    zloc: str = "mid",
    fmt: str = FLOAT_FORMAT,
) -> str:
    """Generate XB values by specifying the center point, width, length, and height."""

    def min_max(i: float, d: float, loc: str) -> tuple[float, float]:
        if loc == "mid":
            values = i - d / 2, i + d / 2
        elif loc == "min":
            values = i, i + d
        elif loc == "max":
            values = i - d, i
        return values

    if len(xyz) != 3:
        raise ValueError(f"XYZ must have 3 values, got {xyz}")

    values: list[float] = []
    for i, d, loc in zip(xyz, (dx, dy, dz), (xloc, yloc, zloc)):
        values.extend(min_max(i, d, loc))

    return xb(values, fmt)


def xyz(values: list[float], fmt: str = FLOAT_FORMAT) -> str:
    """Format values for XYZ parameter."""
    if len(values) != 3:
        raise ValueError(f"XB must have 3 values, got {values}")

    return ",".join([fmt % v for v in values])


def ijk(xb: list[float], res: float, rounding: str = "round") -> str:
    """Determine IJK for &MESH based on XB and resolution."""
    if len(xb) != 6:
        raise ValueError(f"XB must have 6 values, got {xb}")

    values = [abs((xb[ix + 1] - xb[ix]) / res) for ix in range(0, 5, 2)]

    if rounding == "round":
        values = [round(v) for v in values]
    elif rounding == "ceil":
        values = [math.ceil(v) for v in values]
    elif rounding == "floor":
        values = [math.floor(v) for v in values]
    else:
        raise ValueError(
            f"Rounding must be one of ['round', 'ceil', 'floor'], received {rounding}"
        )

    return ",".join([str(v) for v in values])
