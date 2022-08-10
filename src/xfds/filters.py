from __future__ import annotations

import math
from typing import Optional

import numpy as np

from .units import ureg

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

    if rounding == "ceil":
        values = [math.ceil(v) for v in values]
    elif rounding == "floor":
        values = [math.floor(v) for v in values]
    else:
        values = [round(v) for v in values]

    return ",".join([str(v) for v in values])


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a value from one unit to another."""
    return ureg.Quantity(value, from_unit).to(to_unit).magnitude


def str_convert(value: float, from_unit: str, to_unit: str, fmt: str) -> str:
    return fmt % convert(value=value, from_unit=from_unit, to_unit=to_unit)


def arange(step: float, start: float, stop: float) -> list[float]:
    return np.arange(start=start, stop=stop, step=step)


def linspace(num: int, start: float, stop: float, endpoint: bool = True) -> list[float]:
    return np.linspace(start=start, stop=stop, num=num, endpoint=endpoint)


def t2(hrr: float, tg: float = 0, alpha: float = 0) -> float:
    if tg and not alpha:
        alpha = 1000 / tg**2
    return abs(math.sqrt(hrr / alpha)) * -1


def exhaust(flow: float) -> float:
    return abs(flow)


def supply(flow: float) -> float:
    return abs(flow) * -1


def ior(
    axis: str,
    from_device_to_target: Optional[str] = None,
    from_target_to_device: Optional[str] = None,
) -> int:
    axes = "x", "y", "z"
    directions = "-", "+"
    if axis.lower() not in axes:
        raise ValueError(f"Axis must be one of 'x', 'y', or 'z'. Received {axis}")

    if from_device_to_target is None and from_target_to_device is None:
        raise ValueError(
            "You must specify either target direction or device direction as +/- relative to the other."
        )

    if from_device_to_target and from_target_to_device is None:
        if from_device_to_target not in directions:
            raise ValueError("Target direction from device should be +/- along axis.")
        from_target_to_device = "-" if from_device_to_target == "+" else "+"

    if from_target_to_device not in directions:
        raise ValueError("Target direction from device should be +/- along axis.")

    sign = 1 if from_target_to_device == "+" else -1
    return sign * (axes.index(axis) + 1)


def node(cores: int, ppn: int, mode: str = "") -> bool:
    full, part = divmod(cores, ppn)
    modes = ["full", "part", "both"]
    mode = mode.lower()
    if mode not in modes:
        raise ValueError(f"Mode parameter must be one of: {modes}")

    if mode == "full":
        return bool(full)
    elif mode == "part":
        return bool(part)
    else:
        return bool(full) and bool(part)
