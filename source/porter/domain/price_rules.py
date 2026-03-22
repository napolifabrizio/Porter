DROP_THRESHOLD = 0.05


def evaluate_price_drop(initial: float, current: float) -> tuple[bool, float]:
    """Return (dropped, change_pct) where change_pct is (initial - current) / initial."""
    change_pct = (initial - current) / initial
    return change_pct >= DROP_THRESHOLD, change_pct
