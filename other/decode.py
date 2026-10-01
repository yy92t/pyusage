from __future__ import annotations

import sys
import urllib.parse


def main() -> None:
	encoded_url = (
		sys.argv[1]
		if len(sys.argv) > 1
		else "https://news.mingpao.com/ins/%e7%86%b1%e9%bb%9e/article/20241210/s00024/1733573709632"
	)
	decoded_url = urllib.parse.unquote(encoded_url)
	print("Decoded URL:", decoded_url)


if __name__ == "__main__":
	main()
