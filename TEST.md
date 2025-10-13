# Coding Take-Home: Trades & Positions API

## Overview
You're given a SQLite database (`data/trades_takehome.db`) with mock trades for BTC/USD, ETH/USD, SOL/USD.
Build:
1. An HTTP API with two endpoints:
   - `GET /trades` → filtered trades
   - `GET /positions` → net positions (BUY positive, SELL negative)
2. An OpenAPI spec (`openapi.yaml` or `openapi.json`).

You may use any language/framework/tools.

## Requirements

### `GET /trades`
- Params: `account_id` (required), `start_time` (ISO-8601 UTC), `end_time` (ISO-8601 UTC), `symbol` (BTC/USD|ETH/USD|SOL/USD)
- Sort by timestamp ascending
- Return consistent JSON (include fields: trade_id, account_id, symbol, side, price, quantity, ts).
- Nice-to-have: pagination (`page_size`, `page`).

### `GET /positions`
- Params: `account_id` (required), `symbol` (optional)
- Compute net position per symbol: sum(+qty for BUY, -qty for SELL). If `symbol` given, return that only.

### Deliverables
- Source code for the API
- OpenAPI document
- README with setup/run instructions and design notes
- Tests (at least basic unit tests for filtering and position math)
- Anything needed to run the code built on your local machine (i.e. virtual environments)

## Database
File: `data/trades_takehome.db`

Table: `trades`
- trade_id (TEXT, PK)
- account_id (INTEGER)
- symbol (TEXT: BTC/USD | ETH/USD | SOL/USD)
- side (TEXT: BUY | SELL)
- price (REAL)
- quantity (REAL)
- ts (TEXT, ISO-8601 UTC)

Indexes:
- (account_id, ts)
- (symbol, ts)


Any choices not explicitly mentioned in the spec above are up to the developer.

Be ready to explain your choices in the in-person interview.
