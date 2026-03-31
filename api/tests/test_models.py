"""
Tests for Pydantic model validation.
Covers valid data acceptance and invalid data rejection for all key models.
"""
import pytest
from datetime import date, datetime
from decimal import Decimal
from pydantic import ValidationError

from app.models import (
    Customer,
    LineItem,
    LineItemEdit,
    QuoteSummary,
    QuoteDetail,
    QuoteUpdate,
    TemplateSectionConfig,
    TemplateSummary,
    TemplateDetail,
    TemplateCreate,
    TemplateUpdate,
    PreviewRequest,
    RenderRequest,
    TemplatePreviewRequest,
)


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------

class TestCustomer:
    def test_valid_full(self):
        c = Customer(
            customer_id=1,
            company_name="Acme Corp",
            contact_name="Jane Doe",
            contact_email="jane@acme.com",
            phone="555-1234",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip="62701",
            industry="Manufacturing",
        )
        assert c.customer_id == 1
        assert c.company_name == "Acme Corp"
        assert c.industry == "Manufacturing"

    def test_valid_required_only(self):
        c = Customer(customer_id=2, company_name="Minimal Inc")
        assert c.contact_name is None
        assert c.contact_email is None
        assert c.phone is None
        assert c.address is None
        assert c.city is None
        assert c.state is None
        assert c.zip is None
        assert c.industry is None

    def test_missing_customer_id_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            Customer(company_name="No ID Corp")
        errors = exc_info.value.errors()
        fields = [e["loc"][0] for e in errors]
        assert "customer_id" in fields

    def test_missing_company_name_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            Customer(customer_id=1)
        errors = exc_info.value.errors()
        fields = [e["loc"][0] for e in errors]
        assert "company_name" in fields

    def test_invalid_customer_id_type_raises(self):
        with pytest.raises(ValidationError):
            Customer(customer_id="not-an-int", company_name="Bad Corp")


# ---------------------------------------------------------------------------
# LineItem
# ---------------------------------------------------------------------------

class TestLineItem:
    def _valid_data(self):
        return dict(
            line_item_id=10,
            quote_id=1,
            service_category="Hazardous Waste",
            service_description="Drum disposal",
            quantity=Decimal("5"),
            unit="drum",
            unit_price=Decimal("150.00"),
            line_total=Decimal("750.00"),
            sort_order=1,
        )

    def test_valid(self):
        li = LineItem(**self._valid_data())
        assert li.line_item_id == 10
        assert li.line_total == Decimal("750.00")

    def test_quantity_as_string_coerced(self):
        data = self._valid_data()
        data["quantity"] = "3.5"
        li = LineItem(**data)
        assert li.quantity == Decimal("3.5")

    def test_unit_price_as_float_coerced(self):
        data = self._valid_data()
        data["unit_price"] = 99.99
        li = LineItem(**data)
        assert li.unit_price == pytest.approx(Decimal("99.99"), abs=Decimal("0.001"))

    def test_missing_required_field_raises(self):
        data = self._valid_data()
        del data["service_category"]
        with pytest.raises(ValidationError) as exc_info:
            LineItem(**data)
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "service_category" in fields

    def test_invalid_sort_order_type_raises(self):
        data = self._valid_data()
        data["sort_order"] = "not-an-int"
        with pytest.raises(ValidationError):
            LineItem(**data)


# ---------------------------------------------------------------------------
# LineItemEdit
# ---------------------------------------------------------------------------

class TestLineItemEdit:
    def test_valid_all_fields(self):
        lie = LineItemEdit(
            line_item_id=5,
            quantity=Decimal("2"),
            unit_price=Decimal("200.00"),
            service_description="Updated description",
        )
        assert lie.line_item_id == 5
        assert lie.quantity == Decimal("2")

    def test_valid_id_only(self):
        lie = LineItemEdit(line_item_id=5)
        assert lie.quantity is None
        assert lie.unit_price is None
        assert lie.service_description is None

    def test_missing_line_item_id_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            LineItemEdit(quantity=Decimal("1"))
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "line_item_id" in fields

    def test_invalid_quantity_type_raises(self):
        with pytest.raises(ValidationError):
            LineItemEdit(line_item_id=1, quantity="not-a-number")


# ---------------------------------------------------------------------------
# QuoteSummary
# ---------------------------------------------------------------------------

class TestQuoteSummary:
    def test_valid(self):
        qs = QuoteSummary(
            quote_id=100,
            quote_number="Q-2026-001",
            customer_name="Acme Corp",
            status="draft",
            total=Decimal("1500.00"),
            quote_date=date(2026, 1, 15),
        )
        assert qs.quote_number == "Q-2026-001"
        assert qs.status == "draft"
        assert qs.total == Decimal("1500.00")

    def test_quote_date_as_string(self):
        qs = QuoteSummary(
            quote_id=101,
            quote_number="Q-2026-002",
            customer_name="Beta LLC",
            status="sent",
            total="2000.50",
            quote_date="2026-03-15",
        )
        assert qs.quote_date == date(2026, 3, 15)

    def test_missing_quote_number_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            QuoteSummary(
                quote_id=1,
                customer_name="X",
                status="draft",
                total=Decimal("0"),
                quote_date=date.today(),
            )
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "quote_number" in fields

    def test_missing_status_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            QuoteSummary(
                quote_id=1,
                quote_number="Q-001",
                customer_name="X",
                total=Decimal("0"),
                quote_date=date.today(),
            )
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "status" in fields

    def test_invalid_total_raises(self):
        with pytest.raises(ValidationError):
            QuoteSummary(
                quote_id=1,
                quote_number="Q-001",
                customer_name="X",
                status="draft",
                total="not-a-decimal",
                quote_date=date.today(),
            )


# ---------------------------------------------------------------------------
# QuoteUpdate
# ---------------------------------------------------------------------------

class TestQuoteUpdate:
    def test_all_none_is_valid(self):
        qu = QuoteUpdate()
        assert qu.notes is None
        assert qu.regulatory_notes is None
        assert qu.line_items is None

    def test_notes_only(self):
        qu = QuoteUpdate(notes="Some notes here")
        assert qu.notes == "Some notes here"
        assert qu.regulatory_notes is None

    def test_with_line_items(self):
        qu = QuoteUpdate(
            notes="Updated",
            line_items=[
                {"line_item_id": 1, "quantity": "3"},
                {"line_item_id": 2, "unit_price": "99.00"},
            ],
        )
        assert len(qu.line_items) == 2
        assert qu.line_items[0].line_item_id == 1
        assert qu.line_items[0].quantity == Decimal("3")

    def test_invalid_line_item_in_list_raises(self):
        with pytest.raises(ValidationError):
            QuoteUpdate(
                line_items=[{"quantity": "3"}]  # missing line_item_id
            )

    def test_regulatory_notes_set(self):
        qu = QuoteUpdate(regulatory_notes="EPA regulation XYZ applies.")
        assert qu.regulatory_notes == "EPA regulation XYZ applies."


# ---------------------------------------------------------------------------
# TemplateSectionConfig
# ---------------------------------------------------------------------------

class TestTemplateSectionConfig:
    def test_valid_defaults(self):
        tsc = TemplateSectionConfig(section_type="header", label="Header")
        assert tsc.enabled is True
        assert tsc.sort_order == 0
        assert tsc.config is None

    def test_valid_full(self):
        tsc = TemplateSectionConfig(
            section_type="line_items",
            label="Services",
            enabled=True,
            sort_order=3,
            config={"show_totals": True, "columns": ["description", "qty", "price"]},
        )
        assert tsc.sort_order == 3
        assert tsc.config["show_totals"] is True

    def test_missing_section_type_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplateSectionConfig(label="Header")
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "section_type" in fields

    def test_missing_label_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplateSectionConfig(section_type="header")
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "label" in fields


# ---------------------------------------------------------------------------
# TemplateCreate
# ---------------------------------------------------------------------------

class TestTemplateCreate:
    def _section(self):
        return TemplateSectionConfig(section_type="header", label="Header")

    def test_valid(self):
        tc = TemplateCreate(
            template_name="Standard Quote",
            template_key="standard",
            description="Default template",
            style_config={"font": "Arial", "primary_color": "#003366"},
            sections=[self._section()],
        )
        assert tc.template_key == "standard"
        assert len(tc.sections) == 1

    def test_optional_fields_default_none(self):
        tc = TemplateCreate(
            template_name="Minimal",
            template_key="minimal",
            sections=[],
        )
        assert tc.description is None
        assert tc.style_config is None

    def test_missing_template_name_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplateCreate(template_key="key", sections=[])
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "template_name" in fields

    def test_missing_template_key_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplateCreate(template_name="Name", sections=[])
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "template_key" in fields

    def test_missing_sections_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplateCreate(template_name="Name", template_key="key")
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "sections" in fields

    def test_invalid_section_in_list_raises(self):
        with pytest.raises(ValidationError):
            TemplateCreate(
                template_name="Name",
                template_key="key",
                sections=[{"label": "No Type"}],  # missing section_type
            )


# ---------------------------------------------------------------------------
# PreviewRequest
# ---------------------------------------------------------------------------

class TestPreviewRequest:
    def test_valid_no_edits(self):
        pr = PreviewRequest(quote_id=1, template_key="standard")
        assert pr.quote_id == 1
        assert pr.template_key == "standard"
        assert pr.edits is None

    def test_valid_with_edits(self):
        pr = PreviewRequest(
            quote_id=2,
            template_key="detailed",
            edits={"notes": "Updated notes", "line_items": None},
        )
        assert pr.edits.notes == "Updated notes"
        assert pr.edits.line_items is None

    def test_missing_quote_id_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            PreviewRequest(template_key="standard")
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "quote_id" in fields

    def test_missing_template_key_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            PreviewRequest(quote_id=1)
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "template_key" in fields

    def test_invalid_edits_type_raises(self):
        with pytest.raises(ValidationError):
            # edits must be a dict/QuoteUpdate, not a plain string
            PreviewRequest(quote_id=1, template_key="standard", edits="bad-value")

    def test_edits_with_line_items(self):
        pr = PreviewRequest(
            quote_id=3,
            template_key="standard",
            edits={
                "line_items": [
                    {"line_item_id": 10, "quantity": "2", "unit_price": "500.00"}
                ]
            },
        )
        assert len(pr.edits.line_items) == 1
        assert pr.edits.line_items[0].line_item_id == 10


# ---------------------------------------------------------------------------
# RenderRequest
# ---------------------------------------------------------------------------

class TestRenderRequest:
    def test_valid_pdf(self):
        rr = RenderRequest(quote_id=1, template_key="standard", format="pdf")
        assert rr.format == "pdf"

    def test_valid_docx(self):
        rr = RenderRequest(quote_id=1, template_key="standard", format="docx")
        assert rr.format == "docx"

    def test_missing_format_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            RenderRequest(quote_id=1, template_key="standard")
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "format" in fields

    def test_with_edits(self):
        rr = RenderRequest(
            quote_id=5,
            template_key="detailed",
            format="pdf",
            edits={"notes": "Final version"},
        )
        assert rr.edits.notes == "Final version"


# ---------------------------------------------------------------------------
# TemplatePreviewRequest
# ---------------------------------------------------------------------------

class TestTemplatePreviewRequest:
    def test_valid_no_style(self):
        tpr = TemplatePreviewRequest(
            sections=[TemplateSectionConfig(section_type="header", label="Header")]
        )
        assert len(tpr.sections) == 1
        assert tpr.style_config is None

    def test_valid_with_style(self):
        tpr = TemplatePreviewRequest(
            sections=[],
            style_config={"primary_color": "#ff0000"},
        )
        assert tpr.style_config["primary_color"] == "#ff0000"

    def test_missing_sections_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            TemplatePreviewRequest()
        fields = [e["loc"][0] for e in exc_info.value.errors()]
        assert "sections" in fields
