import markdown

CSS_TEMPLATE = """
<style>
@page {{
    size: letter;
    margin: 1in;
}}
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
}}
h1, h2, h3 {{ color: var(--primary-color); }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; table-layout: fixed; }}
th {{ background: var(--primary-color); color: white; padding: 10px; text-align: left; white-space: nowrap; }}
td {{ padding: 8px 10px; border-bottom: 1px solid #ddd; word-wrap: break-word; overflow-wrap: break-word; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
/* Services table column widths */
th:nth-child(1) {{ width: 15%; }}
th:nth-child(2) {{ width: 35%; white-space: normal; }}
th:nth-child(3) {{ width: 8%; text-align: right; }}
th:nth-child(4) {{ width: 8%; }}
th:nth-child(5) {{ width: 14%; text-align: right; }}
th:nth-child(6) {{ width: 14%; text-align: right; }}
td:nth-child(3), td:nth-child(5), td:nth-child(6) {{ text-align: right; white-space: nowrap; }}
td:nth-child(4) {{ white-space: nowrap; }}
</style>
"""

def render_html(markdown_text: str, style_config: dict | None = None) -> str:
    config = style_config or {}
    primary_color = config.get("color_scheme", "#1a365d")
    font_family = config.get("font_family", "Calibri")

    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    css = CSS_TEMPLATE.format(primary_color=primary_color, font_family=font_family)

    return f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{html_body}</body></html>"
