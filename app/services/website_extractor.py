from typing import Dict
import httpx
from bs4 import BeautifulSoup
from app.config import settings


class WebsiteExtractionError(Exception):
    pass


async def fetch_and_extract_website(url: str) -> Dict[str, str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        async with httpx.AsyncClient(
            timeout=settings.request_timeout,
            follow_redirects=True,
            max_redirects=5,
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise WebsiteExtractionError("Website request timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise WebsiteExtractionError(
            f"Website returned HTTP {exc.response.status_code}."
        ) from exc
    except httpx.RequestError as exc:
        raise WebsiteExtractionError(f"Failed to connect to website: {str(exc)}") from exc

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        raise WebsiteExtractionError(f"Unsupported content type: {content_type}")

    soup = BeautifulSoup(response.text, "lxml")

    # Remove noise tags to reduce LLM token cost
    for tag in soup(["script", "style", "noscript", "svg", "iframe", "canvas"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    headings = []
    for h_tag in soup.find_all(["h1", "h2", "h3"]):
        text = " ".join(h_tag.get_text(" ", strip=True).split())
        if text and text not in headings:
            headings.append(f"{h_tag.name.upper()}: {text}")

    # Extract clean deduplicated paragraphs/list items
    seen_lines = set()
    body_chunks = []
    for elem in soup.find_all(["p", "li", "article", "section"]):
        line = " ".join(elem.get_text(" ", strip=True).split())
        if len(line) > 25 and line not in seen_lines:
            seen_lines.add(line)
            body_chunks.append(line)

    clean_body = "\n".join(body_chunks)[: settings.max_content_chars]

    if not title and not headings and len(clean_body) < 50:
        raise WebsiteExtractionError(
            "Insufficient readable text extracted from the website (possibly JS-rendered or blocked)."
        )

    return {
        "url": str(response.url),
        "title": title,
        "meta_description": meta_desc,
        "headings": "\n".join(headings[:40]),
        "body_text": clean_body,
    }