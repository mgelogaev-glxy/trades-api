# Trades & Positions API

FastAPI-based REST API for querying trades and positions from SQLite database.

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API:
```bash
uvicorn api:app --reload
```

Server runs at `http://localhost:8000`

## API Examples

### GET /trades
Get filtered trades for an account.

**Request:**
```bash
curl "http://localhost:8000/trades?account_id=1001&page_size=2"
```

**Response:**
```json
[
  {
    "trade_id": "LX69DO4AKE5U",
    "account_id": 1001,
    "symbol": "SOL/USD",
    "side": "BUY",
    "price": 145.65,
    "quantity": 21.8219,
    "ts": "2025-08-01T00:19:30Z"
  },
  {
    "trade_id": "MBGAB7U3OA87",
    "account_id": 1001,
    "symbol": "SOL/USD",
    "side": "BUY",
    "price": 146.54,
    "quantity": 30.1645,
    "ts": "2025-08-02T10:26:25Z"
  }
]
```

**Parameters:**
- `account_id` (required): Account ID
- `start_time` (optional): ISO-8601 UTC timestamp
- `end_time` (optional): ISO-8601 UTC timestamp
- `symbol` (optional): BTC/USD, ETH/USD, or SOL/USD
- `page_size` (optional): Results per page (default: 20, max: 100)
- `page` (optional): Page number (default: 1)

### GET /positions
Get net positions by symbol for an account.

**Request:**
```bash
curl "http://localhost:8000/positions?account_id=1001"
```

**Response:**
```json
[
  {
    "symbol": "BTC/USD",
    "net_position": 0.4243
  },
  {
    "symbol": "ETH/USD",
    "net_position": -6.8189
  },
  {
    "symbol": "SOL/USD",
    "net_position": -93.7545
  }
]
```

**Parameters:**
- `account_id` (required): Account ID
- `symbol` (optional): Filter by specific symbol

## Testing

Run tests:
```bash
pytest test_api.py -v
```

## Design Notes

**Framework**: FastAPI
- Auto-generated OpenAPI docs at `/docs`
- Type validation with Pydantic
- Fast async performance

**Database**: SQLite with `sqlite3`
- Single connection per request
- Indexed queries on `(account_id, ts)` and `(symbol, ts)`
- Row factory for dict conversion

**Position Calculation**: SQL aggregation
- `SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END)`
- Computed in database for efficiency

**Pagination**: Offset-based
- Simple LIMIT/OFFSET implementation
- Works well for small-medium datasets# trades-api
