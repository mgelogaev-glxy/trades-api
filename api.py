from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List, Dict
import db

app = FastAPI(
    title="Trades & Positions API",
    description="API for trades and nets",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message":"Trades & Postions",
        "version":"1.0.0",
        "status":"running"
    }


@app.get("/trades", response_model=List[Dict])
def get_trades(
    account_id: int = Query(..., description="Account ID (required)"),
    start_time: Optional[str] = Query(None, description="Start time (ISO-8601 UTC)"),
    end_time: Optional[str] = Query(None, description="End time (ISO-8601 UTC)"),
    symbol: Optional[str] = Query(None, description="Trading symbol (BTC/USD, ETH/USD, SOL/USD)"),
    page_size: int = Query(20, description="Number of results per page (100 is default)", ge=1, le=100),
    page: int = Query(1, description="Page number (# is default)", ge=1)
):
    try:
        trades = db.get_trades(
            account_id=account_id, 
            start_time=start_time,
            end_time=end_time,
            symbol=symbol,
            page_size = page_size,
            page = page
        )
        return trades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/positions", response_model=List[Dict])
def get_positions(
    account_id: int = Query(..., description="Account ID (required)"),
    symbol: Optional[str] = Query(None, description="Trading symbol (BTC/USD, ETH/USD, SOL/USD)")
):
    try:
        positions = db.get_positions(
            account_id=account_id,
            symbol=symbol
        )
        return positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
