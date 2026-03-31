from pathlib import Path

SECTIONS_DIR = Path(__file__).parent / "templates" / "sections"

SECTION_MAP = {
    "header": "header.md.j2",
    "summary": "summary_section.md.j2",
    "line_items": "line_items.md.j2",
    "regulatory": "regulatory.md.j2",
    "terms": "terms.md.j2",
    "signature": "signature.md.j2",
}

def compile_template(sections: list[dict], style_config: dict | None = None) -> str:
    enabled = [s for s in sections if s.get("enabled", True)]
    enabled.sort(key=lambda s: s.get("sort_order", 0))

    parts = []
    for section in enabled:
        section_type = section["section_type"]
        filename = SECTION_MAP.get(section_type)
        if filename:
            snippet_path = SECTIONS_DIR / filename
            if snippet_path.exists():
                parts.append(snippet_path.read_text())

    return "\n\n".join(parts)
