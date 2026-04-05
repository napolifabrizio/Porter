# Coding Patterns — Porter

## 1. Always type every field, parameter, and return value

Every method parameter, return type, and object field must have an explicit type annotation. Never leave anything untyped.

**Bad**
```python
class CheckResult:
    product = None
    dropped = False
    change_pct = 0
    error = None

def check_one(self, product):
    html = self._fetcher.fetch(product.url)
    return html
```

**Good**
```python
@dataclass
class CheckResult:
    product: Product
    dropped: bool
    change_pct: float
    error: str | None
    scraped_by_llm: bool = False

def _check_one(self, product: Product) -> CheckResult:
    html: str = self._fetcher.fetch(product.url)
    return CheckResult(...)
```

This also applies to Pydantic models, Protocol methods, and local variables where the type is not immediately obvious from context.

```python
# Protocol — all params and return types annotated
class ProductRepository(Protocol):
    def add_product(self, scraped: ScrapedData, url: str) -> Product: ...
    def list_products(self) -> list[Product]: ...
    def update_price(self, product_id: int, new_price: float) -> None: ...

# Pydantic model — every field annotated, optionals use `X | None`
class Product(BaseModel):
    id: int
    url: str
    name: str
    description: str | None
    initial_price: float
    current_price: float
    last_checked: str
```

## 2. Component design principles

Every component (class, module, or layer) must follow these five principles:

1. **Well-defined boundaries** — a component exposes a clear interface and hides its internals. Nothing outside should depend on implementation details.
- applications files with yours `ports`

2. **Composability** — components are designed to be combined. Dependencies are injected, not hard-coded, so they can be swapped or extended freely.
- Only dependency injection, you can see it in class `PriceChecker`

3. **Independence** — a component does not know about the existence of other concrete components. It only knows about the abstractions (Protocols) it needs.
- applications files with yours `ports`
- Each file in infrastructure doesnt know the others files

4. **State isolation** — a component owns its own state and does not share mutable state with others. Side effects are explicit and contained.

## 3. Naming

1. `method` -> snake_case (def good_example)
2. `Class` -> PascalCase (class GoodExample)
3. `Class attributes` -> _ + camelCase (self._goodExample or self._repo)
4. `Constants` -> UPPER CASE (GOOD_EXAMPLE)
