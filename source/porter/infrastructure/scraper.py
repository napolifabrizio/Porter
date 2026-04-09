import json
import re

from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from porter.models import ScrapedData


class _LLMProduct(BaseModel):
    name: str
    price_raw: str
    description: str | None = None


_ISO_TO_SYMBOL: dict[str, str] = {
    "BRL": "R$",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
}


class Scraper:
    @staticmethod
    def _extract_currency(raw: str) -> str:
        """Extract a currency display symbol from a raw price string."""
        if "R$" in raw:
            return "R$"
        for symbol in ("$", "€", "£", "¥"):
            if symbol in raw:
                return symbol
        return "R$"

    @staticmethod
    def _normalize_price(raw: str) -> float:
        """Normalize price strings like 'R$ 1.299,99', '$12.99', '€1,299.00' to float."""
        cleaned = re.sub(r"[^\d.,]", "", raw).strip()
        if not cleaned:
            raise ValueError(f"Could not parse price from: {raw!r}")

        # European format: dot as thousands separator, comma as decimal (e.g. 1.299,99)
        if "," in cleaned and "." in cleaned:
            if cleaned.rindex(".") < cleaned.rindex(","):
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        elif "," in cleaned:
            # Only comma present — treat as decimal separator (e.g. 1299,99)
            parts = cleaned.split(",")
            if len(parts) == 2 and len(parts[1]) <= 2:
                cleaned = cleaned.replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")

        try:
            return float(cleaned)
        except ValueError:
            raise ValueError(f"Could not parse price from: {raw!r}")

    def _scrape_with_json_ld(self, html: str) -> ScrapedData | None:
        """Try to extract product data from JSON-LD structured data (<script type='application/ld+json'>)."""
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
            except (json.JSONDecodeError, AttributeError):
                continue

            # Normalize to a flat list of items (handles @graph and bare arrays)
            if isinstance(data, dict) and "@graph" in data:
                items = data["@graph"]
            elif isinstance(data, list):
                items = data
            else:
                items = [data]

            for item in items:
                if not isinstance(item, dict):
                    continue
                item_type = item.get("@type", "")
                if isinstance(item_type, list):
                    is_product = "Product" in item_type
                else:
                    is_product = item_type in (
                        "Product",
                        "http://schema.org/Product",
                        "https://schema.org/Product",
                    )
                if not is_product:
                    continue

                name = item.get("name") or None
                description = item.get("description") or None

                # offers can be a single dict or a list
                price_raw = None
                offers = item.get("offers")
                if isinstance(offers, list):
                    offers = offers[0] if offers else None
                price_currency: str | None = None
                if isinstance(offers, dict):
                    raw = offers.get("price")
                    price_raw = str(raw) if raw is not None else None
                    iso_code = offers.get("priceCurrency")
                    if iso_code:
                        price_currency = _ISO_TO_SYMBOL.get(iso_code)

                if not name or not price_raw:
                    continue

                try:
                    price = self._normalize_price(price_raw)
                except ValueError:
                    continue

                if price_currency is None:
                    price_currency = self._extract_currency(price_raw)

                return ScrapedData(name=name, price=price, description=description, currency=price_currency)

        return None

    def _scrape_with_bs4(self, html: str) -> ScrapedData | None:
        """Try to extract product data using common CSS selectors. Returns None if incomplete."""
        soup = BeautifulSoup(html, "html.parser")

        # --- price ---
        price_raw: str | None = None
        for selector in [
            ".a-price .a-offscreen",             # Amazon: accessible span with full price e.g. "$459.99"
            "#priceblock_ourprice",              # Amazon legacy
            "#priceblock_dealprice",             # Amazon deal legacy
            "[itemprop='price']",
            "meta[property='og:price:amount']",
            "[class*='price_vista-']",           # Brazilian e-commerce: PIX/cash promotional price
            "[class*='sale-price']",
            "[class*='special-price']",
            "[class*='promo-price']",
            "[class*='price']",
        ]:
            el = soup.select_one(selector)
            if el:
                # Normalize hyphens → underscores so both "price-original" and "price_original" match
                classes = " ".join(el.get("class", [])).lower().replace("-", "_")
                if any(skip in classes for skip in ("_from", "_old", "_original", "_before", "strikethrough")):
                    continue
                price_raw = el.get("content") or el.get_text(strip=True)
                if price_raw:
                    break

        # Fallback: data-* price attributes used by some storefronts
        if not price_raw:
            for attr in ("data-sale-price", "data-price", "data-product-price"):
                el = soup.select_one(f"[{attr}]")
                if el:
                    price_raw = el.get(attr)
                    if price_raw:
                        break

        # --- name ---
        name: str | None = None
        for selector in ["[itemprop='name']", "meta[property='og:title']", "h1"]:
            el = soup.select_one(selector)
            if el:
                name = el.get("content") or el.get_text(strip=True)
                if name:
                    # Strip "Product Name | Site Name" — pipe is almost always a site-name separator
                    if "|" in name:
                        name = name.split("|")[0].strip()
                    break

        # --- description ---
        description: str | None = None
        for selector in [
            "meta[property='og:description']",
            "meta[name='description']",
            "[itemprop='description']",
        ]:
            el = soup.select_one(selector)
            if el:
                description = el.get("content") or el.get_text(strip=True)
                if description:
                    break

        if not price_raw or not name:
            return None

        currency = self._extract_currency(price_raw)

        try:
            price = self._normalize_price(price_raw)
        except ValueError:
            return None

        return ScrapedData(name=name, price=price, description=description, currency=currency)

    def _scrape_with_llm(self, html: str) -> ScrapedData:
        """Extract product data using LangChain LLM when BS4 fails."""
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        text = text[:8000]

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        structured_llm = llm.with_structured_output(_LLMProduct)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a product data extractor. Given raw text from a product page, "
                "extract the product name, current selling price (as a raw string including currency symbol), "
                "and a short description. If there is a promotional or sale price, use that instead of the original price. "
                "If a field is not found, omit it.",
            ),
            ("human", "{page_text}"),
        ])

        chain = prompt | structured_llm
        result: _LLMProduct = chain.invoke({"page_text": text})

        currency = self._extract_currency(result.price_raw)
        price = self._normalize_price(result.price_raw)
        return ScrapedData(name=result.name, price=price, description=result.description, scraped_by_llm=True, currency=currency)

    def scrape(self, html: str) -> ScrapedData:
        """Extract product data from HTML using hybrid strategy."""
        result = self._scrape_with_json_ld(html)
        if result is not None:
            return result

        result = self._scrape_with_bs4(html)
        if result is not None:
            return result

        return self._scrape_with_llm(html)
