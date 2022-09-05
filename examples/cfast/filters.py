def hrr(t: int, tg: int) -> float:
    """Get the heat release rate at time t following a t-squared growth curve."""
    if t < tg:
        return 1000.0 * (t / tg) ** 2
    else:
        return 1000.0
