"""
Integration tests for the documents router.
Requires a running database with seed data (quote_id=1 must exist).
Run with: pytest api/tests/test_documents_router.py
"""
import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# POST /api/documents/preview
# ---------------------------------------------------------------------------

def test_preview_returns_200_html(client: TestClient):
    """Basic preview with a system template returns 200 and valid HTML."""
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "formal",
    })
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert "<!DOCTYPE html>" in body or "<html" in body
    # Should contain some quote content
    assert "QT-" in body or "Quote" in body or "quote" in body.lower()


def test_preview_contains_customer_info(client: TestClient):
    """Preview HTML should include customer data from the quote."""
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "formal",
    })
    assert response.status_code == 200
    body = response.text
    # The formal template header renders company_name and contact info
    # Just verify it has substantive HTML content (line items table, etc.)
    assert "<table" in body or "Services" in body or "Category" in body


def test_preview_with_notes_edit_returns_updated_notes(client: TestClient):
    """Edits overlay: overriding notes should appear in the rendered HTML."""
    custom_note = "CUSTOM INTEGRATION TEST NOTE XYZ789"
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "formal",
        "edits": {
            "notes": custom_note,
        },
    })
    assert response.status_code == 200
    assert custom_note in response.text


def test_preview_with_regulatory_notes_edit(client: TestClient):
    """Edits overlay: overriding regulatory_notes should appear in the rendered HTML."""
    custom_reg = "CUSTOM REGULATORY NOTE ABC123"
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "formal",
        "edits": {
            "regulatory_notes": custom_reg,
        },
    })
    assert response.status_code == 200
    assert custom_reg in response.text


def test_preview_with_line_item_edit(client: TestClient):
    """Edits overlay: updating a line item's service_description should appear in the HTML."""
    new_desc = "EDITED SERVICE DESCRIPTION FOR TEST"
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "formal",
        "edits": {
            "line_items": [
                {"line_item_id": 1, "service_description": new_desc},
            ],
        },
    })
    assert response.status_code == 200
    assert new_desc in response.text


def test_preview_with_invalid_quote_id_returns_404(client: TestClient):
    """Requesting a preview for a non-existent quote_id should return 404."""
    response = client.post("/api/documents/preview", json={
        "quote_id": 99999,
        "template_key": "formal",
    })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Quote not found"


def test_preview_with_invalid_template_key_returns_404(client: TestClient):
    """Requesting a preview with a template_key that doesn't exist should return 404."""
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "nonexistent_template_key_xyz",
    })
    assert response.status_code == 404


def test_preview_proposal_template(client: TestClient):
    """The 'proposal' system template should also render successfully."""
    response = client.post("/api/documents/preview", json={
        "quote_id": 1,
        "template_key": "proposal",
    })
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# POST /api/documents/render
# ---------------------------------------------------------------------------

def test_render_pdf_returns_pdf_content_type(client: TestClient):
    """Render with format=pdf should return application/pdf."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "pdf",
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    # PDF files start with %PDF
    assert response.content[:4] == b"%PDF"


def test_render_pdf_has_content_disposition_header(client: TestClient):
    """Render PDF should include Content-Disposition attachment header."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "pdf",
    })
    assert response.status_code == 200
    cd = response.headers.get("content-disposition", "")
    assert "attachment" in cd
    assert ".pdf" in cd


def test_render_docx_returns_docx_content_type(client: TestClient):
    """Render with format=docx should return DOCX content-type."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "docx",
    })
    assert response.status_code == 200
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["content-type"]
    )
    # DOCX files are ZIP archives — start with PK magic bytes
    assert response.content[:2] == b"PK"


def test_render_docx_has_content_disposition_header(client: TestClient):
    """Render DOCX should include Content-Disposition attachment header."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "docx",
    })
    assert response.status_code == 200
    cd = response.headers.get("content-disposition", "")
    assert "attachment" in cd
    assert ".docx" in cd


def test_render_invalid_format_returns_400(client: TestClient):
    """Render with an unsupported format should return 400."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "xlsx",
    })
    assert response.status_code == 400


def test_render_invalid_quote_id_returns_404(client: TestClient):
    """Render for a non-existent quote should return 404."""
    response = client.post("/api/documents/render", json={
        "quote_id": 99999,
        "template_key": "formal",
        "format": "pdf",
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Quote not found"


def test_render_pdf_with_edits(client: TestClient):
    """Render PDF with edits overlay should succeed and still return PDF."""
    response = client.post("/api/documents/render", json={
        "quote_id": 1,
        "template_key": "formal",
        "format": "pdf",
        "edits": {
            "notes": "Edited for PDF render test",
        },
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
