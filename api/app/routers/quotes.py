from fastapi import APIRouter, HTTPException
from app.database import fetch_all, fetch_one, execute
from app.models import QuoteSummary, QuoteDetail, QuoteUpdate, Customer, LineItem
from datetime import datetime
import json

router = APIRouter(prefix="/api/quotes", tags=["quotes"])

@router.get("/", response_model=list[QuoteSummary])
def list_quotes():
    rows = fetch_all("""
        SELECT q.quote_id, q.quote_number, c.company_name AS customer_name,
               q.status, q.total, q.quote_date
        FROM Quotes q JOIN Customers c ON q.customer_id = c.customer_id
        ORDER BY q.quote_date DESC
    """)
    return rows

@router.get("/{quote_id}", response_model=QuoteDetail)
def get_quote(quote_id: int):
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
        customer_id=quote["customer_id"], company_name=quote["company_name"],
        contact_name=quote["contact_name"], contact_email=quote["contact_email"],
        phone=quote["phone"], address=quote["address"], city=quote["city"],
        state=quote["state"], zip=quote["zip"], industry=quote["industry"]
    )

    return QuoteDetail(
        quote_id=quote["quote_id"], quote_number=quote["quote_number"],
        customer=customer, quote_date=quote["quote_date"],
        valid_until=quote["valid_until"], status=quote["status"],
        subtotal=quote["subtotal"], tax_rate=quote["tax_rate"],
        tax_amount=quote["tax_amount"], total=quote["total"],
        notes=quote["notes"], regulatory_notes=quote["regulatory_notes"],
        line_items=[LineItem(**item) for item in items],
        created_at=quote["created_at"], updated_at=quote["updated_at"]
    )

@router.put("/{quote_id}", response_model=QuoteDetail)
def update_quote(quote_id: int, update: QuoteUpdate):
    existing = fetch_one("SELECT quote_id FROM Quotes WHERE quote_id = ?", (quote_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Quote not found")

    if update.notes is not None:
        execute("UPDATE Quotes SET notes = ?, updated_at = SYSUTCDATETIME() WHERE quote_id = ?",
                (update.notes, quote_id))
    if update.regulatory_notes is not None:
        execute("UPDATE Quotes SET regulatory_notes = ?, updated_at = SYSUTCDATETIME() WHERE quote_id = ?",
                (update.regulatory_notes, quote_id))

    if update.line_items:
        for item_edit in update.line_items:
            fields, values = [], []
            if item_edit.quantity is not None:
                fields.append("quantity = ?")
                values.append(item_edit.quantity)
            if item_edit.unit_price is not None:
                fields.append("unit_price = ?")
                values.append(item_edit.unit_price)
            if item_edit.service_description is not None:
                fields.append("service_description = ?")
                values.append(item_edit.service_description)
            if fields:
                fields.append("line_total = ISNULL(?, quantity) * ISNULL(?, unit_price)")
                values.extend([item_edit.quantity, item_edit.unit_price])
                values.append(item_edit.line_item_id)
                execute(f"UPDATE QuoteLineItems SET {', '.join(fields)} WHERE line_item_id = ?", tuple(values))

        execute("""
            UPDATE Quotes SET
                subtotal = (SELECT ISNULL(SUM(line_total), 0) FROM QuoteLineItems WHERE quote_id = ?),
                tax_amount = (SELECT ISNULL(SUM(line_total), 0) FROM QuoteLineItems WHERE quote_id = ?) * tax_rate,
                total = (SELECT ISNULL(SUM(line_total), 0) FROM QuoteLineItems WHERE quote_id = ?) * (1 + tax_rate),
                updated_at = SYSUTCDATETIME()
            WHERE quote_id = ?
        """, (quote_id, quote_id, quote_id, quote_id))

    return get_quote(quote_id)
