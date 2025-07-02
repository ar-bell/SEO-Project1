import sqlite3
import json 

DBFile = "cryptoinsights.db"

def init_db(path: str = DBFile) -> sqlite3.connection:
    """
    Making sure we have a database + table, then return out.
    """
    conn = sqlite3.connect(path)
    conn.execute("""
    Create table for favorites data .... (updating later)
    """
    conn.commit()
    return conn 
