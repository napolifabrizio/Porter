# Domain

The `domain/` folder contains the **core business rules** of Porter — pure logic with no I/O, no framework dependencies, and no imports from other layers.

## Responsibility

This layer answers the question: *"Given a price, has it dropped (or risen) enough to matter?"*

It owns the price-change thresholds and the formulas that evaluate them. Nothing outside this folder decides what counts as a significant price movement.

## Contents

### `price_rules.py`
Defines `DROP_THRESHOLD = 0.05` (5%) and `evaluate_price_drop(initial, current)`, which returns whether the current price has dropped at least 5% from the initial price and by how much.

## Design principles

- **No side effects.** Functions are pure: same inputs always produce the same output.
- **No dependencies.** This module imports nothing from the rest of the project. The dependency arrow always points inward — `ui → application → domain`, never the reverse.
- **Single source of truth for thresholds.** If the drop threshold ever changes, it changes here and only here.

---

## Adding a new domain rule

When you need to add or change a business rule (e.g. a rise threshold, a staleness check, a discount cap), follow these three steps.

### Step 1 — Add the constant and function to `domain/`

Place new rules in `price_rules.py` if they relate to price evaluation, or create a new file if the concern is distinct (e.g. `domain/staleness_rules.py`). Define thresholds as module-level constants so they remain a single source of truth.

```python
# domain/price_rules.py
RISE_THRESHOLD = 0.05

def evaluate_price_rise(initial: float, current: float) -> tuple[bool, float]:
    """Return (risen, change_pct) where change_pct is (current - initial) / initial."""
    change_pct = (current - initial) / initial
    return change_pct >= RISE_THRESHOLD, change_pct
```

### Step 2 — Keep the function pure

Domain functions must have **no side effects and no I/O**. They must not import from `application/`, `infrastructure/`, or `ui/`. Inputs and outputs are plain Python primitives or dataclasses — never ORM objects, HTTP responses, or Pydantic models that belong to another layer.

```python
# Good — pure function, no imports from other layers
def evaluate_price_rise(initial: float, current: float) -> tuple[bool, float]: ...

# Bad — imports from application layer, introduces I/O dependency
from porter.application.ports import ProductRepository  # never do this
```

### Step 3 — Call it from the application layer

Domain functions are consumed exclusively by `application/checker.py` (or other application-layer orchestrators). Import the function there and wire its result into `CheckResult` or whatever DTO the caller needs.

```python
# application/checker.py
from porter.domain.price_rules import evaluate_price_drop, evaluate_price_rise

dropped, drop_pct = evaluate_price_drop(product.initial_price, scraped.price)
risen, rise_pct   = evaluate_price_rise(product.initial_price, scraped.price)
```

No file outside `application/` should import from `domain/` directly — the dependency arrow is `ui → application → domain`, not `ui → domain`.
