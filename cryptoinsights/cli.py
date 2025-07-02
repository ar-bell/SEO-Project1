#!/usr/bin/env python3
"""
Welcome to CryptoInsights. 
""" 
from dotenv import load_dotenv 
load_dotenv()

import argparse
from rich import print 
from rich.console import Console 

from clients.newsdata import NewsDataClient 
from clients.coinpaprika import CoinPaprikaClient

console = Console()

def main():
    parser = argparse.ArgumentParser(prog="cryptoinsights")
    parser.add_argument("--coin", required=True, help="slug like btc-bitcoin")
    parser.add_argument("--since", default="24h", choices=["24h"])
    args = parser.parse_args()
    
    print(
        f"[bold dark_magenta]Great! :rocket:  Environment has loaded.[/bold dark_magenta] "
        f"[bold dark_magenta]Here is your coin:[bold /dark_magenta] "
        f"[bright_green]{args.coin}[/bright_green]\n"
        )

    cp = CoinPaprikaClient()
    price = cp.get_price(args.coin)
    print(
        f"[purple4]:moneybag: {args.coin.title()} Price:[/purple4] "
        f"[bold bright_green]${price['current']:.2f} [/bold bright_green] "
        f"[purple4]24h Change:[/purple4] "
        f"[bold bright_green] {price['change_percent']}%[/bold bright_green]\n"
        )


    nd = NewsDataClient()
    raw = nd.get_headlines(args.coin, count=5)
    seen = set()
    headlines = []
    for title in raw: 
        if title not in seen: 
            seen.add(title)
            headlines.append(title)
        if len(headlines) == 3:
            break
        

    print("[bold red]Top 3 Headlines: [/bold red]")
    for h in headlines:
        print(f"[orange]• {h} [/orange]")

if __name__ == "__main__":
    main()

