"""
PDF renderer tests using WeasyPrint.
NOTE: WeasyPrint requires system libraries (cairo, pango).
These tests will only pass inside the Docker container and may be skipped locally.
"""
import pytest


def test_render_pdf_returns_pdf_bytes():
    try:
        from app.renderers.pdf_renderer import render_pdf
    except ImportError:
        pytest.skip("WeasyPrint not available in this environment")

    result = render_pdf("<html><body><h1>Test</h1></body></html>")
    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF"), "Output should be a valid PDF (starts with %PDF)"
