from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from decimal import Decimal
import copy
import json

from jinja2 import Environment, FileSystemLoader

from app.models import PreviewRequest, RenderRequest
from app.database import fetch_all, fetch_one
from app.renderers.html_renderer import render_html
from app.renderers.pdf_renderer import render_pdf
from app.renderers.docx_renderer import render_docx
from app.template_compiler import compile_template

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Templates directory is at app/templates/ (sibling of this file's parent)
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

template_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def _to_decimal(value) -> Decimal:
    """Coerce a value to Decimal for arithmetic in templates."""
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def _build_quote_namespace(quote_detail) -> SimpleNamespace:
    """
    Convert a QuoteDetail Pydantic model into a nested SimpleNamespace tree
    so Jinja2 templates can use dot notation (quote.customer.company_name)
    and call strftime on date fields.
    """
    # Build customer namespace
    c = quote_detail.customer
    customer_ns = SimpleNamespace(
        customer_id=c.customer_id,
        company_name=c.company_name,
        contact_name=c.contact_name,
        contact_email=c.contact_email,
        phone=c.phone,
        address=c.address,
        city=c.city,
        state=c.state,
        zip=c.zip,
        industry=c.industry,
    )

    # Build line item namespaces — Decimal values preserved for arithmetic
    line_item_nss = []
    for li in quote_detail.line_items:
        line_item_nss.append(SimpleNamespace(
            line_item_id=li.line_item_id,
            quote_id=li.quote_id,
            service_category=li.service_category,
            service_description=li.service_description,
            quantity=_to_decimal(li.quantity),
            unit=li.unit,
            unit_price=_to_decimal(li.unit_price),
            line_total=_to_decimal(li.line_total),
            sort_order=li.sort_order,
        ))

    # Top-level quote namespace — dates are kept as date objects so strftime works
    quote_ns = SimpleNamespace(
        quote_id=quote_detail.quote_id,
        quote_number=quote_detail.quote_number,
        customer=customer_ns,
        quote_date=quote_detail.quote_date,
        valid_until=quote_detail.valid_until,
        status=quote_detail.status,
        subtotal=_to_decimal(quote_detail.subtotal),
        tax_rate=_to_decimal(quote_detail.tax_rate),
        tax_amount=_to_decimal(quote_detail.tax_amount),
        total=_to_decimal(quote_detail.total),
        notes=quote_detail.notes,
        regulatory_notes=quote_detail.regulatory_notes,
        line_items=line_item_nss,
        created_at=quote_detail.created_at,
        updated_at=quote_detail.updated_at,
    )

    return quote_ns


def _apply_edits(quote_detail, edits) -> object:
    """
    Return a copy of quote_detail with edits applied (non-persisting overlay).
    edits is a QuoteUpdate model (notes, regulatory_notes, line_items overrides).
    """
    if edits is None:
        return quote_detail

    # Deep-copy via dict round-trip to avoid mutating the original
    from app.models import QuoteDetail, Customer, LineItem

    # Rebuild a mutable copy
    customer_copy = quote_detail.customer.model_copy()

    line_items_copy = [li.model_copy() for li in quote_detail.line_items]

    detail_copy = quote_detail.model_copy(update={
        "customer": customer_copy,
        "line_items": line_items_copy,
    })

    # Apply top-level field overrides
    if edits.notes is not None:
        detail_copy = detail_copy.model_copy(update={"notes": edits.notes})
    if edits.regulatory_notes is not None:
        detail_copy = detail_copy.model_copy(update={"regulatory_notes": edits.regulatory_notes})

    # Apply line item overrides
    if edits.line_items:
        edit_map = {e.line_item_id: e for e in edits.line_items}
        new_items = []
        for li in detail_copy.line_items:
            if li.line_item_id in edit_map:
                item_edit = edit_map[li.line_item_id]
                update_fields = {}
                if item_edit.quantity is not None:
                    update_fields["quantity"] = item_edit.quantity
                if item_edit.unit_price is not None:
                    update_fields["unit_price"] = item_edit.unit_price
                if item_edit.service_description is not None:
                    update_fields["service_description"] = item_edit.service_description
                # Recalculate line_total if quantity or unit_price changed
                qty = update_fields.get("quantity", li.quantity)
                price = update_fields.get("unit_price", li.unit_price)
                update_fields["line_total"] = _to_decimal(qty) * _to_decimal(price)
                new_items.append(li.model_copy(update=update_fields))
            else:
                new_items.append(li)

        # Recalculate subtotal / tax_amount / total
        subtotal = sum(_to_decimal(li.line_total) for li in new_items)
        tax_amount = subtotal * _to_decimal(detail_copy.tax_rate)
        total = subtotal + tax_amount

        detail_copy = detail_copy.model_copy(update={
            "line_items": new_items,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total": total,
        })

    return detail_copy


def _load_quote(quote_id: int):
    """Fetch and construct a QuoteDetail from the database, or raise 404."""
    from app.models import QuoteDetail, Customer, LineItem

    quote = fetch_one("""
        SELECT q.*, c.customer_id, c.company_name, c.contact_name, c.contact_email,
               c.phone, c.address, c.city, c.state, c.zip, c.industry
        FROM Quotes q JOIN Customers c ON q.customer_id = c.customer_id
        WHERE q.quote_id = ?
    """, (quote_id,))
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    items = fetch_all("""
        SELECT * FROM QuoteLineItems WHERE quote_id = ? ORDER BY sort_order
    """, (quote_id,))

    customer = Customer(
        customer_id=quote["customer_id"],
        company_name=quote["company_name"],
        contact_name=quote["contact_name"],
        contact_email=quote["contact_email"],
        phone=quote["phone"],
        address=quote["address"],
        city=quote["city"],
        state=quote["state"],
        zip=quote["zip"],
        industry=quote["industry"],
    )

    return QuoteDetail(
        quote_id=quote["quote_id"],
        quote_number=quote["quote_number"],
        customer=customer,
        quote_date=quote["quote_date"],
        valid_until=quote["valid_until"],
        status=quote["status"],
        subtotal=quote["subtotal"],
        tax_rate=quote["tax_rate"],
        tax_amount=quote["tax_amount"],
        total=quote["total"],
        notes=quote["notes"],
        regulatory_notes=quote["regulatory_notes"],
        line_items=[LineItem(**item) for item in items],
        created_at=quote["created_at"],
        updated_at=quote["updated_at"],
    )


def _resolve_template_and_style(template_key: str) -> tuple[str | None, dict | None, bool]:
    """
    Resolve a template_key to a rendered Jinja2 template string source and
    its associated style_config.

    Returns (jinja2_template_source_string, style_config_dict_or_None).

    Strategy:
      1. If a file <template_key>.md.j2 exists in TEMPLATES_DIR, use it as a
         system file template (style_config from DB if available, else None).
      2. Otherwise, look up the template in the DB by template_key and compile
         from its sections via template_compiler.
    """
    system_file = TEMPLATES_DIR / f"{template_key}.md.j2"
    if system_file.exists():
        # Use the Jinja2 file-based template; try to get style_config from DB
        style_config = None
        db_row = fetch_one(
            "SELECT style_config FROM QuoteTemplates WHERE template_key = ?",
            (template_key,),
        )
        if db_row and db_row.get("style_config"):
            try:
                style_config = json.loads(db_row["style_config"])
            except (json.JSONDecodeError, TypeError):
                pass
        # Return None for source — caller will use template_env.get_template
        return None, style_config, True  # (source, style_config, is_file_template)

    # DB-based user template: compile from sections
    db_row = fetch_one(
        "SELECT * FROM QuoteTemplates WHERE template_key = ?",
        (template_key,),
    )
    if not db_row:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_key}' not found",
        )

    style_config = None
    if db_row.get("style_config"):
        try:
            style_config = json.loads(db_row["style_config"])
        except (json.JSONDecodeError, TypeError):
            pass

    sections_rows = fetch_all(
        "SELECT * FROM TemplateSections WHERE template_id = ? ORDER BY sort_order",
        (db_row["template_id"],),
    )

    sections_dicts = []
    for s in sections_rows:
        config = None
        if s.get("config"):
            try:
                config = json.loads(s["config"])
            except (json.JSONDecodeError, TypeError):
                pass
        sections_dicts.append({
            "section_type": s["section_type"],
            "label": s["label"],
            "enabled": bool(s["enabled"]),
            "sort_order": s["sort_order"],
            "config": config,
        })

    template_source = compile_template(sections_dicts, style_config)
    return template_source, style_config, False  # (source, style_config, is_file_template)


def _render_markdown(template_key: str, quote_ns: SimpleNamespace) -> tuple[str, dict | None]:
    """
    Render the Jinja2 template for the given template_key with the quote
    namespace as context.  Returns (markdown_string, style_config).
    """
    source, style_config, is_file_template = _resolve_template_and_style(template_key)

    if is_file_template:
        tmpl = template_env.get_template(f"{template_key}.md.j2")
    else:
        tmpl = template_env.from_string(source)

    markdown_text = tmpl.render(quote=quote_ns)
    return markdown_text, style_config


@router.post("/preview", response_class=HTMLResponse)
def preview_document(request: PreviewRequest):
    quote_detail = _load_quote(request.quote_id)
    quote_detail = _apply_edits(quote_detail, request.edits)
    quote_ns = _build_quote_namespace(quote_detail)

    markdown_text, style_config = _render_markdown(request.template_key, quote_ns)
    html = render_html(markdown_text, style_config)
    return HTMLResponse(content=html)


@router.post("/render")
def render_document(request: RenderRequest):
    if request.format not in ("pdf", "docx"):
        raise HTTPException(status_code=400, detail="format must be 'pdf' or 'docx'")

    quote_detail = _load_quote(request.quote_id)
    quote_detail = _apply_edits(quote_detail, request.edits)
    quote_ns = _build_quote_namespace(quote_detail)

    markdown_text, style_config = _render_markdown(request.template_key, quote_ns)
    html = render_html(markdown_text, style_config)

    quote_number = quote_ns.quote_number.replace("/", "-").replace("\\", "-")

    if request.format == "pdf":
        pdf_bytes = render_pdf(html)
        filename = f"{quote_number}.pdf"
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    else:  # docx
        # Build quote_data dict for the styled python-docx renderer
        quote_data = {
            "quote_number": quote_detail.quote_number,
            "quote_date": str(quote_detail.quote_date),
            "valid_until": str(quote_detail.valid_until),
            "status": quote_detail.status,
            "subtotal": quote_detail.subtotal,
            "tax_rate": quote_detail.tax_rate,
            "tax_amount": quote_detail.tax_amount,
            "total": quote_detail.total,
            "notes": quote_detail.notes,
            "regulatory_notes": quote_detail.regulatory_notes,
            "customer": {
                "company_name": quote_detail.customer.company_name,
                "contact_name": quote_detail.customer.contact_name,
                "contact_email": quote_detail.customer.contact_email,
                "industry": quote_detail.customer.industry,
            },
            "line_items": [
                {
                    "service_category": li.service_category,
                    "service_description": li.service_description,
                    "quantity": li.quantity,
                    "unit": li.unit,
                    "unit_price": li.unit_price,
                    "line_total": li.line_total,
                }
                for li in quote_detail.line_items
            ],
        }
        docx_bytes = render_docx(html, quote_data=quote_data, style_config=style_config)
        filename = f"{quote_number}.docx"
        return StreamingResponse(
            BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
