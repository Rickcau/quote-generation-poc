"""
Integration tests for the customers router.
Requires a running database with seed data.
Run with: pytest api/tests/test_customers_router.py
"""
from fastapi.testclient import TestClient


def test_list_customers_returns_200_and_list(client: TestClient):
    response = client.get("/api/customers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Validate shape of first item
    first = data[0]
    assert "customer_id" in first
    assert "company_name" in first
    assert "contact_name" in first
    assert "contact_email" in first
    assert "phone" in first
    assert "address" in first
    assert "city" in first
    assert "state" in first
    assert "zip" in first
    assert "industry" in first
