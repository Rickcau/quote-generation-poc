"""
Integration tests for the templates router.
Requires a running database with seed data (3 system templates).
Run with: pytest api/tests/test_templates_router.py
"""
import pytest
from fastapi.testclient import TestClient

# Template ID to use for non-destructive read tests (seed data has IDs 1-3)
_READ_TEMPLATE_ID = 1


def test_list_templates_returns_200_and_list(client: TestClient):
    response = client.get("/api/templates/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert "template_id" in first
    assert "template_name" in first
    assert "template_key" in first
    assert "is_default" in first
    assert "is_system" in first


def test_get_template_detail_returns_200_with_sections(client: TestClient):
    response = client.get(f"/api/templates/{_READ_TEMPLATE_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["template_id"] == _READ_TEMPLATE_ID
    assert "template_name" in data
    assert "template_key" in data
    assert "is_default" in data
    assert "is_system" in data
    assert "updated_at" in data
    assert "sections" in data
    assert isinstance(data["sections"], list)
    # Seed data has sections for system templates
    assert len(data["sections"]) > 0
    section = data["sections"][0]
    assert "section_type" in section
    assert "label" in section
    assert "enabled" in section
    assert "sort_order" in section


def test_get_template_not_found_returns_404(client: TestClient):
    response = client.get("/api/templates/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Template not found"


def test_create_template_returns_201(client: TestClient):
    payload = {
        "template_name": "Test Template",
        "template_key": "test_template_pytest",
        "description": "Created by pytest",
        "style_config": {"color_scheme": "#336699", "font_family": "Arial"},
        "sections": [
            {
                "section_type": "header",
                "label": "Header",
                "enabled": True,
                "sort_order": 1,
                "config": None,
            },
            {
                "section_type": "line_items",
                "label": "Line Items",
                "enabled": True,
                "sort_order": 2,
                "config": None,
            },
            {
                "section_type": "signature",
                "label": "Signature",
                "enabled": True,
                "sort_order": 3,
                "config": None,
            },
        ],
    }
    response = client.post("/api/templates/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["template_name"] == "Test Template"
    assert data["template_key"] == "test_template_pytest"
    assert data["description"] == "Created by pytest"
    assert data["style_config"] == {"color_scheme": "#336699", "font_family": "Arial"}
    assert data["is_system"] is False
    assert isinstance(data["sections"], list)
    assert len(data["sections"]) == 3
    assert "template_id" in data
    # Clean up: delete the created template so tests are idempotent
    created_id = data["template_id"]
    client.delete(f"/api/templates/{created_id}")


def test_update_template_returns_updated_data(client: TestClient):
    # First create a template to update
    create_payload = {
        "template_name": "Update Test Template",
        "template_key": "update_test_pytest",
        "description": "Original description",
        "style_config": None,
        "sections": [
            {
                "section_type": "header",
                "label": "Header",
                "enabled": True,
                "sort_order": 1,
                "config": None,
            }
        ],
    }
    create_resp = client.post("/api/templates/", json=create_payload)
    assert create_resp.status_code == 201
    created_id = create_resp.json()["template_id"]

    try:
        update_payload = {
            "template_name": "Updated Template Name",
            "description": "Updated description",
            "sections": [
                {
                    "section_type": "header",
                    "label": "Header",
                    "enabled": True,
                    "sort_order": 1,
                    "config": None,
                },
                {
                    "section_type": "summary",
                    "label": "Summary",
                    "enabled": True,
                    "sort_order": 2,
                    "config": None,
                },
            ],
        }
        response = client.put(f"/api/templates/{created_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["template_name"] == "Updated Template Name"
        assert data["description"] == "Updated description"
        assert len(data["sections"]) == 2
    finally:
        client.delete(f"/api/templates/{created_id}")


def test_delete_system_template_returns_400(client: TestClient):
    # Template ID 1 is a system template from seed data
    response = client.delete(f"/api/templates/{_READ_TEMPLATE_ID}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete system template"


def test_delete_nonexistent_template_returns_404(client: TestClient):
    response = client.delete("/api/templates/99999")
    assert response.status_code == 404


def test_preview_template_returns_html(client: TestClient):
    payload = {
        "sections": [
            {
                "section_type": "header",
                "label": "Header",
                "enabled": True,
                "sort_order": 1,
                "config": None,
            },
            {
                "section_type": "line_items",
                "label": "Line Items",
                "enabled": True,
                "sort_order": 2,
                "config": None,
            },
        ],
        "style_config": {"color_scheme": "#1a365d", "font_family": "Calibri"},
    }
    response = client.post("/api/templates/preview", json=payload)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert "<!DOCTYPE html>" in body
    assert "<body>" in body


def test_preview_route_not_treated_as_template_id(client: TestClient):
    """Ensures /preview is not misrouted as /{template_id}."""
    payload = {
        "sections": [
            {
                "section_type": "header",
                "label": "Header",
                "enabled": True,
                "sort_order": 1,
                "config": None,
            }
        ],
        "style_config": None,
    }
    response = client.post("/api/templates/preview", json=payload)
    # Should not return 422 (which would happen if "preview" were treated as an int template_id)
    assert response.status_code != 422
    assert response.status_code == 200
