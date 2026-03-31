from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal

# --- Customers ---
class Customer(BaseModel):
    customer_id: int
    company_name: str
    contact_name: str | None = None
    contact_email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    industry: str | None = None

# --- Line Items ---
class LineItem(BaseModel):
    line_item_id: int
    quote_id: int
    service_category: str
    service_description: str
    quantity: Decimal
    unit: str
    unit_price: Decimal
    line_total: Decimal
    sort_order: int

class LineItemEdit(BaseModel):
    line_item_id: int
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    service_description: str | None = None

# --- Quotes ---
class QuoteSummary(BaseModel):
    quote_id: int
    quote_number: str
    customer_name: str
    status: str
    total: Decimal
    quote_date: date

class QuoteDetail(BaseModel):
    quote_id: int
    quote_number: str
    customer: Customer
    quote_date: date
    valid_until: date
    status: str
    subtotal: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total: Decimal
    notes: str | None = None
    regulatory_notes: str | None = None
    line_items: list[LineItem]
    created_at: datetime
    updated_at: datetime

class QuoteUpdate(BaseModel):
    notes: str | None = None
    regulatory_notes: str | None = None
    line_items: list[LineItemEdit] | None = None

# --- Templates ---
class TemplateSectionConfig(BaseModel):
    section_type: str
    label: str
    enabled: bool = True
    sort_order: int = 0
    config: dict | None = None

class TemplateSummary(BaseModel):
    template_id: int
    template_name: str
    template_key: str
    description: str | None = None
    is_default: bool
    is_system: bool

class TemplateDetail(BaseModel):
    template_id: int
    template_name: str
    template_key: str
    description: str | None = None
    style_config: dict | None = None
    is_default: bool
    is_system: bool
    sections: list[TemplateSectionConfig]
    updated_at: datetime

class TemplateCreate(BaseModel):
    template_name: str
    template_key: str
    description: str | None = None
    style_config: dict | None = None
    sections: list[TemplateSectionConfig]

class TemplateUpdate(BaseModel):
    template_name: str | None = None
    description: str | None = None
    style_config: dict | None = None
    sections: list[TemplateSectionConfig] | None = None

# --- Documents ---
class PreviewRequest(BaseModel):
    quote_id: int
    template_key: str
    edits: QuoteUpdate | None = None

class RenderRequest(BaseModel):
    quote_id: int
    template_key: str
    format: str  # "pdf" or "docx"
    edits: QuoteUpdate | None = None

class TemplatePreviewRequest(BaseModel):
    sections: list[TemplateSectionConfig]
    style_config: dict | None = None
