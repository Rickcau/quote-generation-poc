"""
Integration tests for the quotes router.
Requires a running database with seed data.
Run with: pytest api/tests/test_quotes_router.py
"""
import pytest
from fastapi.testclient import TestClient


def test_list_quotes_returns_200_and_list(client: TestClient):
    response = client.get("/api/quotes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Validate shape of first item
    first = data[0]
    assert "quote_id" in first
    assert "quote_number" in first
    assert "customer_name" in first
    assert "status" in first
    assert "total" in first
    assert "quote_date" in first


def test_get_quote_detail_returns_200_with_customer_and_line_items(client: TestClient):
    response = client.get("/api/quotes/1")
    assert response.status_code == 200
    data = response.json()
    # Top-level quote fields
    assert data["quote_id"] == 1
    assert "quote_number" in data
    assert "status" in data
    assert "subtotal" in data
    assert "tax_rate" in data
    assert "tax_amount" in data
    assert "total" in data
    # Nested customer object
    assert "customer" in data
    customer = data["customer"]
    assert "customer_id" in customer
    assert "company_name" in customer
    assert "contact_name" in customer
    assert "contact_email" in customer
    # Line items list
    assert "line_items" in data
    assert isinstance(data["line_items"], list)
    assert len(data["line_items"]) > 0
    item = data["line_items"][0]
    assert "line_item_id" in item
    assert "service_description" in item
    assert "quantity" in item
    assert "unit_price" in item
    assert "line_total" in item


def test_get_quote_not_found_returns_404(client: TestClient):
    response = client.get("/api/quotes/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Quote not found"


def test_update_quote_notes_returns_updated_quote(client: TestClient):
    updated_notes = "Integration test note update"
    response = client.put("/api/quotes/1", json={"notes": updated_notes})
    assert response.status_code == 200
    data = response.json()
    assert data["quote_id"] == 1
    assert data["notes"] == updated_notes
    # Ensure the full quote detail structure is returned
    assert "customer" in data
    assert "line_items" in data
