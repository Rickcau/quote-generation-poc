import markdown

CSS_TEMPLATE = """
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
}}
h1, h2, h3 {{ color: var(--primary-color); }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th {{ background: var(--primary-color); color: white; padding: 10px; text-align: left; }}
td {{ padding: 8px 10px; border-bottom: 1px solid #ddd; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
</style>
"""

def render_html(markdown_text: str, style_config: dict | None = None) -> str:
    config = style_config or {}
    primary_color = config.get("color_scheme", "#1a365d")
    font_family = config.get("font_family", "Calibri")

    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    css = CSS_TEMPLATE.format(primary_color=primary_color, font_family=font_family)

    return f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{html_body}</body></html>"
