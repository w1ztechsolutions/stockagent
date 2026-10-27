"""URL fetch guard + PDF extraction for Phungu Insights tools.

Only fetches http/https URLs. Public-IP resolution rejects private/link-local
addresses so the tool cannot be used for SSRF against the agent's own network.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Any

import httpx

MAX_FETCH_BYTES = 200_000
MAX_TEXT_CHARS = 8_000
FETCH_TIMEOUT = 10.0
USER_AGENT = "Mozilla/5.0 (compatible; PhunguInsightsBot/1.0; +https://mse-portal.wiztechsol-info.workers.dev)"
ALLOWED_SCHEMES = ("http", "https")


def _is_private_ip(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved


def _resolve_public_ips(hostname: str) -> list[str]:
    import socket

    try:
        infos = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        return [addr[4][0] for addr in infos if addr[4][0] and not _is_private_ip(addr[4][0])]
    except (OSError, ValueError):
        return []


def _html_to_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text)


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes. Falls back to a byte-size indicator."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open("pdf", pdf_bytes)
        parts = [doc[page].get_text() for page in range(len(doc))]
        return "\n".join(parts)
    except ImportError:
        return f"[PDF received: {len(pdf_bytes)} bytes - PyMuPDF not available for text extraction]"
    except Exception as exc:
        return f"[PDF extraction error: {exc}]"


def fetch_url(url: str) -> dict[str, Any]:
    """Fetch *url* and return its content.

    Returns a dict with keys: found, url, content_type, content, source.
    On failure: found=False plus an error string.
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ALLOWED_SCHEMES:
            return {"found": False, "url": url, "error": f"scheme {parsed.scheme} not allowed", "source": "fetch_error"}

        host = parsed.hostname or ""
        public_ips = _resolve_public_ips(host)
        if not public_ips and host:
            return {"found": False, "url": url, "error": "host resolves only to private addresses", "source": "fetch_error"}

        response = httpx.get(
            url,
            timeout=FETCH_TIMEOUT,
            headers={"User-Agent": USER_AGENT, "Accept": "application/pdf, text/html, */*"},
            follow_redirects=True,
            max_redirects=5,
        )
        response.raise_for_status()

        content_type = response.headers.get("content-type", "").lower()
        url_lower = url.lower()
        is_pdf = "application/pdf" in content_type or url_lower.endswith(".pdf")

        if is_pdf:
            text = _extract_pdf_text(response.content)
            source = "mse_reports" if "mse.co.mw" in url_lower else "pdf"
        else:
            text = _html_to_text(response.text[:MAX_TEXT_CHARS])
            source = "webpage"

        return {
            "found": True,
            "url": url,
            "content_type": content_type,
            "content": text[:MAX_TEXT_CHARS],
            "source": source,
        }

    except httpx.HTTPError as exc:
        return {"found": False, "url": url, "error": str(exc), "source": "fetch_error"}
    except Exception as exc:
        return {"found": False, "url": url, "error": f"Unexpected error: {exc}", "source": "unexpected_error"}