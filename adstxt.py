from __future__ import annotations

import concurrent.futures
from pathlib import Path
from urllib.parse import urlparse

import requests


WEBSITES: list[str] = [
	"https://www.mingpao.com",
	# "https://www.hk01.com",
]

OUTPUT_DIR = Path("ads_txt_files")


def _domain_from_url(url: str) -> str:
	parsed = urlparse(url)
	return parsed.netloc or parsed.path


def scrape_ads_txt(session: requests.Session, url: str, output_dir: Path) -> Path | None:
	ads_url = f"{url.rstrip('/')}/ads.txt"
	try:
		response = session.get(ads_url, timeout=10)
		if response.status_code != 200:
			print(f"Failed to retrieve ads.txt from {url} (HTTP {response.status_code})")
			return None

		output_dir.mkdir(parents=True, exist_ok=True)
		filename = output_dir / f"{_domain_from_url(url)}.txt"
		filename.write_text(response.text, encoding="utf-8")
		print(f"Successfully saved {filename}")
		return filename
	except requests.RequestException as exc:
		print(f"Error fetching {ads_url}: {exc}")
		return None


def main() -> None:
	if not WEBSITES:
		print("No websites configured.")
		return

	with requests.Session() as session:
		session.headers.update({"User-Agent": "pyusage/1.0"})
		with concurrent.futures.ThreadPoolExecutor(max_workers=min(16, len(WEBSITES))) as pool:
			list(pool.map(lambda u: scrape_ads_txt(session, u, OUTPUT_DIR), WEBSITES))


if __name__ == "__main__":
	main()
