## 1. Refactor checker.py

- [x] 1.1 Extract the per-product check logic from `check_all_prices` into a private `_check_one(product)` method
- [x] 1.2 Replace the sequential `for` loop in `check_all_prices` with a `ThreadPoolExecutor`, submitting `_check_one` for each product
- [x] 1.3 Store futures in a `dict[Future → int]` (index map) and write results into a pre-sized list to preserve input order

## 2. Verify correctness

- [ ] 2.1 Manually run the app and trigger "Check All Prices" with multiple products — confirm all results appear and are in the correct order
- [ ] 2.2 Verify a failed scrape on one product does not prevent others from returning results
