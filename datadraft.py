from __future__ import annotations

import requests
import pandas as pd


URL = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Hong_Kong_Stock_Exchange"


def main() -> None:
    with requests.Session() as session:
        session.headers.update({"User-Agent": "pyusage/1.0"})
        response = session.get(URL, timeout=20)
        response.raise_for_status()

    # pandas.read_html is implemented in optimized code paths and is generally
    # faster (and less error-prone) than manual BeautifulSoup table walking.
    tables = pd.read_html(response.text)
    if not tables:
        raise RuntimeError("No tables found on page")

    df = tables[0]
    df.to_csv("output.csv", index=False)
    print("Data has been scraped and saved to output.csv")


if __name__ == "__main__":
    main()
