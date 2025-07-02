import os
import requests


BASE_URL = "https://newsdata.io/api/1/latest"

class NewsDataClient:
    def __init__(self, session=None):
        self.session = session or requests.Session()
        self.api_key = os.getenv("NEWSDATA_API_KEY")

    def get_headlines(self, query: str, count: int = 3) -> list[str]:
        """
        Grab the latest crypto-related headlines matching `query`.
        Returns up to `count` article titles.
        """
        params = {
            "apikey": self.api_key,
            "q": query,
            "language": "en",
        }

        resp = self.session.get(BASE_URL, params=params, timeout=5)
        resp.raise_for_status()


        items = resp.json().get("results", [])[:count]

        return [item["title"] for item in items]
