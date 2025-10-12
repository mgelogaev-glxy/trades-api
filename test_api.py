import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"

def test_trades_endpoint_requires_account_id():
    response = client.get("/trades")
    assert response.status_code == 422

def test_positions_endpoint_requires_account_id():
    response = client.get("/positions")
    assert response.status_code == 422

def test_trades_endpoint_with_account_id():
    """Test /trades returns data for a valid account."""
    response = client.get("/trades?account_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # If there are trades, verify structure
    if len(data) > 0:
        trade = data[0]
        assert "trade_id" in trade
        assert "account_id" in trade
        assert "symbol" in trade
        assert "side" in trade
        assert "price" in trade
        assert "quantity" in trade
        assert "ts" in trade
        assert trade["account_id"] == 1


def test_trades_endpoint_with_symbol_filter():
    """Test /trades filters by symbol correctly."""
    response = client.get("/trades?account_id=1&symbol=BTC/USD")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # If there are trades, verify they're all BTC/USD
    for trade in data:
        assert trade["symbol"].upper() == "BTC/USD"


def test_positions_endpoint_with_account_id():
    """Test /positions returns data for a valid account."""
    response = client.get("/positions?account_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # If there are positions, verify structure
    if len(data) > 0:
        position = data[0]
        assert "symbol" in position
        assert "net_position" in position
        assert isinstance(position["net_position"], (int, float))


def test_positions_endpoint_with_symbol_filter():
    """Test /positions filters by symbol correctly."""
    response = client.get("/positions?account_id=1&symbol=BTC/USD")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # If there are positions, verify it's only BTC/USD
    for position in data:
        assert position["symbol"].upper() == "BTC/USD"


def test_trades_sorted_by_timestamp():
    """Test that trades are sorted by timestamp ascending."""
    response = client.get("/trades?account_id=1")
    assert response.status_code == 200
    data = response.json()
    
    if len(data) > 1:
        # Check timestamps are in ascending order
        for i in range(len(data) - 1):
            assert data[i]["ts"] <= data[i + 1]["ts"]