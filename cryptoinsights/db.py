import sqlite3
import json

DB_FILE = "cryptoinsights.db"

def init_db(path: str = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS snapshots (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        coin        TEXT    NOT NULL,
        timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
        price       REAL    NOT NULL,
        change_pct  REAL    NOT NULL,
        headlines   TEXT    NOT NULL
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        coin        TEXT    NOT NULL,
        headline    TEXT    NOT NULL,
        saved_at    DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    return conn

def save_snapshot(conn: sqlite3.Connection,
                  coin: str,
                  price: float,
                  change_pct: float,
                  headlines: list[str]) -> None:
    conn.execute(
        "INSERT INTO snapshots (coin, price, change_pct, headlines) VALUES (?, ?, ?, ?)",
        (coin, price, change_pct, json.dumps(headlines))
    )
    conn.commit()

def save_favorites(conn: sqlite3.Connection,
                  coin: str,
                  headline: str) -> None:
    conn.execute(
        "INSERT INTO favorites (coin, headline) VALUES (?, ?)",
        (coin, headline)
    )
    conn.commit()

def list_favorites(conn: sqlite3.Connection,
                   coin: str = None) -> list[tuple]:
    sql = "SELECT id, coin, headline, saved_at FROM favorites"
    params = []
    if coin:
        sql += " WHERE coin = ?"
        params.append(coin)
    sql += " ORDER BY saved_at DESC"
    return conn.execute(sql, params).fetchall()


# pasted in proj docs to edit table formatting

