from __future__ import annotations

from urllib.parse import unquote, urljoin

import requests
from bs4 import BeautifulSoup


def fetch_and_parse(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def extract_and_decode_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links: list[str] = []
    # select('a[href]') is a bit faster than find_all with kwargs.
    for a_tag in soup.select("a[href]"):
        href = a_tag.get("href")
        if not href:
            continue
        link = urljoin(base_url, href)
        links.append(unquote(link))
    return links


def main() -> None:
    url = "https://www.scmp.com"
    with requests.Session() as session:
        session.headers.update({"User-Agent": "pyusage/1.0"})
        soup = fetch_and_parse(session, url)
    links = extract_and_decode_links(soup, url)

    # Display links in chronological order (order of appearance)
    for link in links:
        print(link)


if __name__ == "__main__":
    main()
