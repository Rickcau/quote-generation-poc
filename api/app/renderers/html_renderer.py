import markdown

CSS_BASE = """
<style>
:root {{
    --primary-color: {primary_color};
    --font-family: {font_family};
}}
body {{
    font-family: var(--font-family), 'Segoe UI', sans-serif;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px;
    line-height: 1.6;
    font-size: 11pt;
}}
h1, h2, h3 {{ color: var(--primary-color); }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th {{ background: var(--primary-color); color: white; padding: 8px 6px; text-align: left; font-size: 9pt; }}
td {{ padding: 6px; border-bottom: 1px solid #ddd; font-size: 9pt; word-wrap: break-word; overflow-wrap: break-word; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
td:nth-child(3), td:nth-child(5), td:nth-child(6) {{ text-align: right; }}
th:nth-child(3), th:nth-child(5), th:nth-child(6) {{ text-align: right; }}
/* Signature table */
.signature-table {{ table-layout: auto; border: none; margin-top: 2em; }}
.signature-table td {{ border: none; border-bottom: none; padding: 12px 8px; background: transparent !important; font-size: 10pt; }}
.signature-table .sig-label {{ width: 220px; white-space: nowrap; }}
.signature-table .sig-line {{ border-bottom: 1px solid #333 !important; min-width: 250px; }}
.signature-table tr:nth-child(even) {{ background: transparent; }}
</style>
"""

CSS_PRINT = """
<style>
@page {{
    size: letter;
    margin: 0.75in 0.75in;
}}
body {{
    padding: 0;
    max-width: none;
    font-size: 10pt;
}}
table {{ font-size: 8pt; }}
th {{ font-size: 8pt; padding: 6px 4px; }}
td {{ font-size: 8pt; padding: 4px; }}
</style>
"""


def render_html(markdown_text: str, style_config: dict | None = None) -> str:
    config = style_config or {}
    primary_color = config.get("color_scheme", "#1a365d")
    font_family = config.get("font_family", "Calibri")

    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    css = CSS_BASE.format(primary_color=primary_color, font_family=font_family)

    return f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{html_body}</body></html>"


def render_html_for_pdf(markdown_text: str, style_config: dict | None = None) -> str:
    """Render HTML optimized for PDF generation — tighter spacing, @page margins, no body padding."""
    config = style_config or {}
    primary_color = config.get("color_scheme", "#1a365d")
    font_family = config.get("font_family", "Calibri")

    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    css = CSS_BASE.format(primary_color=primary_color, font_family=font_family)

    return f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}{CSS_PRINT}</head><body>{html_body}</body></html>"
