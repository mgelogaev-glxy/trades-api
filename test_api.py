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
    response = client.get("/trades?account_id=1001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        trade = data[0]
        assert "trade_id" in trade
        assert "account_id" in trade
        assert "symbol" in trade
        assert "side" in trade
        assert "price" in trade
        assert "quantity" in trade
        assert "ts" in trade
        assert trade["account_id"] == 1001


def test_trades_endpoint_with_symbol_filter():
    response = client.get("/trades?account_id=1002&symbol=BTC/USD")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for trade in data:
        assert trade["symbol"].upper() == "BTC/USD"


def test_positions_endpoint_with_account_id():
    response = client.get("/positions?account_id=1003")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        position = data[0]
        assert "symbol" in position
        assert "net_position" in position
        assert isinstance(position["net_position"], (int, float))


def test_positions_endpoint_with_symbol_filter():
    response = client.get("/positions?account_id=1004&symbol=BTC/USD")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for position in data:
        assert position["symbol"].upper() == "BTC/USD"