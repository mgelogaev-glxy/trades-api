import sqlite3
from typing import List, Dict, Optional
from pathlib import Path

DB_PATH = Path("data/trades_takehome.db")

def get_connection() -> sqlite3.Connection:
    #Creates db connection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_trades(
        account_id: int,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        symbol: Optional[str] = None,
        page_size: int = 20,
        page: int = 1
) -> List[Dict]:
    conn = get_connection()    
    cursor = conn.cursor()

    query = "SELECT trade_id, account_id, symbol, side, price, quantity, ts FROM trades WHERE account_id = ?"
    params = [account_id]

    if start_time:
        query += " AND ts >= ?"
        params.append(start_time)
    
    if end_time:
        query += " AND ts <= ?"
        params.append(end_time)

    if symbol:
        query += " AND UPPER(symbol) = UPPER(?)"
        params.append(symbol)

    query += " ORDER BY ts ASC"

    offset = (page - 1) * page_size
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_positions (
        account_id: int,
        symbol: Optional[str] = None,
) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT symbol, SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END) as net_position FROM trades WHERE account_id = ?"    
    
    params = [account_id]

    if symbol:
        query += " AND UPPER(symbol) = UPPER(?)"
        params.append(symbol)

    query += " GROUP BY symbol ORDER BY symbol"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]