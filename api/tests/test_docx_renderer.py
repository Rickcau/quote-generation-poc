"""
DOCX renderer tests using python-docx and htmldocx.
NOTE: These tests may not run locally if dependencies are not installed.
They will run in the Docker container.
"""
import pytest


def test_render_docx_returns_zip_bytes():
    try:
        from app.renderers.docx_renderer import render_docx
    except ImportError:
        pytest.skip("python-docx or htmldocx not available in this environment")

    result = render_docx("<html><body><h1>Test</h1></body></html>")
    assert isinstance(result, bytes)
    assert result[:2] == b"PK", "Output should be a valid DOCX/ZIP file (starts with PK)"
