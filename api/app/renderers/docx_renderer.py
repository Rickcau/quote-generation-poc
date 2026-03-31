from io import BytesIO
from docx import Document
from htmldocx import HtmlToDocx

def render_docx(html_string: str) -> bytes:
    doc = Document()
    parser = HtmlToDocx()
    parser.add_html_to_document(html_string, doc)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()
