import os
import requests

API_KEY = os.getenv("NEWS_API_KEY")

url = "https://newsapi.org/v2/top-headlines"

response = requests.get(
    url,
    params={
        "country": "hk",
        "apiKey": API_KEY
    }
)

data = response.json()

for article in data["articles"][:10]:
    print(article["title"])