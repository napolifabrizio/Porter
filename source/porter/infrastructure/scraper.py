import re

from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from porter.application.ports import HtmlFetcher
from porter.models import ScrapedData


class _LLMProduct(BaseModel):
    name: str
    price_raw: str
    description: str | None = None


class Scraper:
    def __init__(self, fetcher: HtmlFetcher):
        self._fetcher = fetcher

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

    def _scrape_with_bs4(self, html: str) -> ScrapedData | None:
        """Try to extract product data using common CSS selectors. Returns None if incomplete."""
        soup = BeautifulSoup(html, "html.parser")

        # --- price ---
        price_raw: str | None = None
        for selector in [
            "[itemprop='price']",
            "meta[property='og:price:amount']",
            "[class*='price']",
        ]:
            el = soup.select_one(selector)
            if el:
                price_raw = el.get("content") or el.get_text(strip=True)
                if price_raw:
                    break

        # --- name ---
        name: str | None = None
        for selector in ["[itemprop='name']", "meta[property='og:title']", "h1"]:
            el = soup.select_one(selector)
            if el:
                name = el.get("content") or el.get_text(strip=True)
                if name:
                    break

        # --- description ---
        description: str | None = None
        for selector in ["meta[name='description']", "[itemprop='description']"]:
            el = soup.select_one(selector)
            if el:
                description = el.get("content") or el.get_text(strip=True)
                if description:
                    break

        if not price_raw or not name:
            return None

        try:
            price = self._normalize_price(price_raw)
        except ValueError:
            return None

        return ScrapedData(name=name, price=price, description=description)

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
                "extract the product name, price (as a raw string including currency symbol), "
                "and a short description. If a field is not found, omit it.",
            ),
            ("human", "{page_text}"),
        ])

        chain = prompt | structured_llm
        result: _LLMProduct = chain.invoke({"page_text": text})

        price = self._normalize_price(result.price_raw)
        return ScrapedData(name=result.name, price=price, description=result.description)

    def fetch_and_scrape(self, url: str) -> ScrapedData:
        """Fetch URL and extract product data using hybrid strategy."""
        html = self._fetcher.fetch(url)

        result = self._scrape_with_bs4(html)
        if result is not None:
            return result

        return self._scrape_with_llm(html)
