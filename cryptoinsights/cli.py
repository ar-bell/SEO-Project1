#!/usr/bin/env python3
"""
Welcome to CryptoInsights. 
""" 
from dotenv import load_dotenv 
load_dotenv()

import argparse
import json 
from rich import print 
from rich.console import Console 

from clients.newsdata import NewsDataClient 
from clients.coinpaprika import CoinPaprikaClient
from clients.genai import GenAIClient
from db import init_db, save_snapshot, save_favorites, list_favorites

console = Console()

def main():
    parser = argparse.ArgumentParser(prog="cryptoinsights")
    parser.add_argument("--coin", required=True, help="slug like btc-bitcoin")
    parser.add_argument("--since", default="24h", choices=["24h"])
    parser.add_argument("--favorites", type=int, help="Mark one of the Top 3 listed headlines (1, 2 or 3) as a favorite")
    parser.add_argument("--list-favorites", action="store_true", help="List all saved favorites (can also filter by --coin)")
    parser.add_argument("--list-snapshots", action="store_true", help="Show all saved snapshots from the DB")
    args = parser.parse_args()

    if args.list_snapshots:
        conn = init_db()
        cur = conn.execute("SELECT * FROM snapshots ORDER BY timestamp DESC")
        rows = cur.fetchall()
        print("[bold light_pink1]Saved Snapshots: [/bold light_pink1]")
        for rid, coin, ts, price, change, raw in rows:
            headlines = json.loads(raw)
            print(f"{rid}. [{coin} @ {ts}] Price=${price:.2f} Change={change}%")
            for h in headlines:
                print("    • ", h)
        return 

    if args.list_favorites:
        conn = init_db()
        favs = list_favorites(conn, coin=args.coin if args.coin else None)
        print("[bold violet]Here Favorites:[/bold violet]")
        for fid, coin, hl, ts in favs:
            print(f" {fid}. [{coin} @ {ts}] {hl}")
        return 
    
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
    
    conn = init_db()
    save_snapshot(conn, args.coin, price["current"], price["change_percent"], headlines)

    if args.favorites:
        i = args.favorites - 1
        if 0 <= i < len(headlines):
            save_favorites(conn, args.coin, headlines[i])
            print(f"\n[bold light_pink1]✓Saved favorites: [/bold light_pink1] {headlines[i]}")
        else:
            print(f"\n [bold red]!Invalid favorite index: {args.favorite} [/bold red]")

    # 9) AI summary
    prompt = (
        f"Summarize {args.coin} price "
        f"(${price['current']:.2f}, 24h change {price['change_percent']}%) "
        "and these three headlines:\n"
        + "\n".join(f"- {h}" for h in headlines)
    )
    ga = GenAIClient()
    summary = ga.summarize(prompt)
    print(f"\n[bold green]AI Summary:[/bold green] {summary}\n")





if __name__ == "__main__":
    main()

