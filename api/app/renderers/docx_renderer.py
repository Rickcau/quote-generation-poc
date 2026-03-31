import re
from io import BytesIO
from docx import Document
from htmldocx import HtmlToDocx


def _fix_loose_lists(html: str) -> str:
    """Convert loose lists (<li><p>text</p></li>) to tight lists (<li>text</li>)
    so htmldocx renders bullets inline with their text."""
    return re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', html, flags=re.DOTALL)


def render_docx(html_string: str) -> bytes:
    html_string = _fix_loose_lists(html_string)
    doc = Document()
    parser = HtmlToDocx()
    parser.add_html_to_document(html_string, doc)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()
