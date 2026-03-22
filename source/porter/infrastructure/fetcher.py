from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from curl_cffi import requests as curl_requests


class HttpFetcher:
    _BROWSER_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    _TRACKING_PARAMS = {
        "gclid", "gad_source", "gad_campaignid", "gbraid", "wbraid",
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "fbclid", "msclkid", "dclid",
    }

    def _clean_url(self, url: str) -> str:
        parsed = urlparse(url)
        qs = {k: v for k, v in parse_qs(parsed.query, keep_blank_values=True).items()
              if k not in self._TRACKING_PARAMS}
        clean_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=clean_query))

    def fetch(self, url: str) -> str:
        clean = self._clean_url(url)
        try:
            response = curl_requests.get(
                clean,
                impersonate="chrome124",
                headers=self._BROWSER_HEADERS,
                allow_redirects=True,
                timeout=15,
            )
            response.raise_for_status()
        except curl_requests.exceptions.Timeout:
            raise RuntimeError(f"Request timed out: {url}")
        except curl_requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP {e.response.status_code} fetching {url}")
        except curl_requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error fetching {url}: {e}")

        return response.text
