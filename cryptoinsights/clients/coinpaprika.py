import requests


BASE_URL = "https://api.coinpaprika.com/v1/"

class CoinPaprikaClient:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def get_price(self, coin_id: str) -> dict: 
        """
        Returning the following:
            - current: price in USD
            - change_percent: float percent change from the last 24 hours
        """
        url = f"{BASE_URL}/tickers/{coin_id}"
        resp = self.session.get(url, timeout = 5)
        resp.raise_for_status()
        usd = resp.json()["quotes"]["USD"]
        return {
            "current": usd["price"], 
            "change_percent": usd["percent_change_24h"],
        }


