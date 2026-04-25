DROP_THRESHOLD = 0.005
RISE_THRESHOLD = DROP_THRESHOLD


def evaluate_price_drop(initial: float, current: float) -> tuple[bool, bool, float]:
    """Return (dropped, rose, change_pct) where change_pct is (initial - current) / initial."""
    change_pct = (initial - current) / initial
    return change_pct >= DROP_THRESHOLD, change_pct <= -RISE_THRESHOLD, change_pct
