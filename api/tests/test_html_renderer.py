from app.renderers.html_renderer import render_html


def test_render_html_basic_structure():
    result = render_html("# Hello")
    assert "<!DOCTYPE html>" in result
    assert "<h1>Hello</h1>" in result


def test_render_html_default_css_color():
    result = render_html("# Hello")
    assert "#1a365d" in result


def test_render_html_custom_color_scheme():
    result = render_html("# Hello", {"color_scheme": "#ff0000"})
    assert "#ff0000" in result


def test_render_html_table():
    md = "| A | B |\n|---|---|\n| 1 | 2 |"
    result = render_html(md)
    assert "<table>" in result
    assert "<th>" in result
    assert "<td>" in result
