from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
from app.database import fetch_all, fetch_one, execute
from app.models import TemplateSummary, TemplateDetail, TemplateCreate, TemplateUpdate, TemplateSectionConfig, TemplatePreviewRequest
from app.template_compiler import compile_template
from app.renderers.html_renderer import render_html
import json

router = APIRouter(prefix="/api/templates", tags=["templates"])


def _build_template_detail(template_id: int) -> TemplateDetail:
    row = fetch_one(
        "SELECT * FROM QuoteTemplates WHERE template_id = ?",
        (template_id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Template not found")

    sections_rows = fetch_all(
        "SELECT * FROM TemplateSections WHERE template_id = ? ORDER BY sort_order",
        (template_id,)
    )

    style_config = None
    if row.get("style_config"):
        try:
            style_config = json.loads(row["style_config"])
        except (json.JSONDecodeError, TypeError):
            style_config = None

    sections = []
    for s in sections_rows:
        config = None
        if s.get("config"):
            try:
                config = json.loads(s["config"])
            except (json.JSONDecodeError, TypeError):
                config = None
        sections.append(TemplateSectionConfig(
            section_type=s["section_type"],
            label=s["label"],
            enabled=bool(s["enabled"]),
            sort_order=s["sort_order"],
            config=config,
        ))

    return TemplateDetail(
        template_id=row["template_id"],
        template_name=row["template_name"],
        template_key=row["template_key"],
        description=row.get("description"),
        style_config=style_config,
        is_default=bool(row["is_default"]),
        is_system=bool(row["is_system"]),
        sections=sections,
        updated_at=row["updated_at"],
    )


@router.get("/", response_model=list[TemplateSummary])
def list_templates():
    rows = fetch_all(
        "SELECT template_id, template_name, template_key, description, is_default, is_system "
        "FROM QuoteTemplates ORDER BY template_name"
    )
    return [
        TemplateSummary(
            template_id=r["template_id"],
            template_name=r["template_name"],
            template_key=r["template_key"],
            description=r.get("description"),
            is_default=bool(r["is_default"]),
            is_system=bool(r["is_system"]),
        )
        for r in rows
    ]


# IMPORTANT: /preview must be defined BEFORE /{template_id}
@router.post("/preview", response_class=HTMLResponse)
def preview_template(request: TemplatePreviewRequest):
    sample_quote = {
        "quote_number": "QT-PREVIEW-001",
        "quote_date": "2026-03-31",
        "valid_until": "2026-04-30",
        "status": "Draft",
        "subtotal": "12500.00",
        "tax_rate": "0.08",
        "tax_amount": "1000.00",
        "total": "13500.00",
        "notes": "Sample preview quote — not a real document.",
        "regulatory_notes": "All waste disposal subject to state regulations.",
        "customer": {
            "company_name": "Acme Industrial Corp",
            "contact_name": "Jane Smith",
            "contact_email": "jane.smith@acme.com",
            "phone": "555-867-5309",
            "address": "100 Factory Lane",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701",
            "industry": "Manufacturing",
        },
        "line_items": [
            {
                "service_category": "Hazardous Waste",
                "service_description": "Drum disposal — flammable liquids",
                "quantity": "10",
                "unit": "drums",
                "unit_price": "750.00",
                "line_total": "7500.00",
                "sort_order": 1,
            },
            {
                "service_category": "Transport",
                "service_description": "Hazmat transport — licensed carrier",
                "quantity": "1",
                "unit": "trip",
                "unit_price": "3000.00",
                "line_total": "3000.00",
                "sort_order": 2,
            },
            {
                "service_category": "Remediation",
                "service_description": "Site assessment and cleanup",
                "quantity": "2",
                "unit": "days",
                "unit_price": "1000.00",
                "line_total": "2000.00",
                "sort_order": 3,
            },
        ],
    }

    sections_dicts = [s.model_dump() for s in request.sections]
    markdown_text = compile_template(sections_dicts, request.style_config)
    html = render_html(markdown_text, request.style_config)
    return HTMLResponse(content=html)


@router.get("/{template_id}", response_model=TemplateDetail)
def get_template(template_id: int):
    return _build_template_detail(template_id)


@router.post("/", response_model=TemplateDetail, status_code=201)
def create_template(payload: TemplateCreate):
    style_config_str = json.dumps(payload.style_config) if payload.style_config is not None else None

    row = fetch_one(
        """
        INSERT INTO QuoteTemplates (template_name, template_key, description, style_config, is_default, is_system)
        OUTPUT INSERTED.template_id
        VALUES (?, ?, ?, ?, 0, 0)
        """,
        (payload.template_name, payload.template_key, payload.description, style_config_str),
    )
    if not row:
        raise HTTPException(status_code=500, detail="Failed to create template")

    template_id = row["template_id"]

    for section in payload.sections:
        config_str = json.dumps(section.config) if section.config is not None else None
        execute(
            """
            INSERT INTO TemplateSections (template_id, section_type, label, enabled, sort_order, config)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (template_id, section.section_type, section.label, int(section.enabled), section.sort_order, config_str),
        )

    return _build_template_detail(template_id)


@router.put("/{template_id}", response_model=TemplateDetail)
def update_template(template_id: int, payload: TemplateUpdate):
    existing = fetch_one("SELECT template_id FROM QuoteTemplates WHERE template_id = ?", (template_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Template not found")

    update_fields = []
    update_values = []

    if payload.template_name is not None:
        update_fields.append("template_name = ?")
        update_values.append(payload.template_name)
    if payload.description is not None:
        update_fields.append("description = ?")
        update_values.append(payload.description)
    if payload.style_config is not None:
        update_fields.append("style_config = ?")
        update_values.append(json.dumps(payload.style_config))

    if update_fields:
        update_fields.append("updated_at = SYSUTCDATETIME()")
        update_values.append(template_id)
        execute(
            f"UPDATE QuoteTemplates SET {', '.join(update_fields)} WHERE template_id = ?",
            tuple(update_values),
        )

    if payload.sections is not None:
        execute("DELETE FROM TemplateSections WHERE template_id = ?", (template_id,))
        for section in payload.sections:
            config_str = json.dumps(section.config) if section.config is not None else None
            execute(
                """
                INSERT INTO TemplateSections (template_id, section_type, label, enabled, sort_order, config)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (template_id, section.section_type, section.label, int(section.enabled), section.sort_order, config_str),
            )

    return _build_template_detail(template_id)


@router.delete("/{template_id}", status_code=204)
def delete_template(template_id: int):
    row = fetch_one(
        "SELECT template_id, is_system FROM QuoteTemplates WHERE template_id = ?",
        (template_id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Template not found")

    if row["is_system"]:
        raise HTTPException(status_code=400, detail="Cannot delete system template")

    execute("DELETE FROM QuoteTemplates WHERE template_id = ?", (template_id,))
    return Response(status_code=204)
