from app.template_compiler import compile_template

def test_compile_all_sections_enabled():
    sections = [
        {"section_type": "header", "label": "Header", "enabled": True, "sort_order": 1, "config": None},
        {"section_type": "line_items", "label": "Line Items", "enabled": True, "sort_order": 2, "config": None},
        {"section_type": "signature", "label": "Signature", "enabled": True, "sort_order": 3, "config": None},
    ]
    result = compile_template(sections, style_config=None)
    assert "header.md.j2" in result or "header" in result.lower()
    assert "line_items" in result.lower()
    assert "signature" in result.lower()

def test_compile_disabled_section_excluded():
    sections = [
        {"section_type": "header", "label": "Header", "enabled": True, "sort_order": 1, "config": None},
        {"section_type": "regulatory", "label": "Regulatory", "enabled": False, "sort_order": 2, "config": None},
    ]
    result = compile_template(sections, style_config=None)
    assert "header" in result.lower()
    assert "regulatory" not in result.lower()

def test_compile_respects_sort_order():
    sections = [
        {"section_type": "signature", "label": "Signature", "enabled": True, "sort_order": 2, "config": None},
        {"section_type": "header", "label": "Header", "enabled": True, "sort_order": 1, "config": None},
    ]
    result = compile_template(sections, style_config=None)
    header_pos = result.lower().find("header")
    sig_pos = result.lower().find("signature")
    assert header_pos < sig_pos
