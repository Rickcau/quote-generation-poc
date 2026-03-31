export interface Customer {
  customer_id: number;
  company_name: string;
  contact_name: string | null;
  contact_email: string | null;
  phone: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  zip: string | null;
  industry: string | null;
}

export interface LineItem {
  line_item_id: number;
  quote_id: number;
  service_category: string;
  service_description: string;
  quantity: number;
  unit: string;
  unit_price: number;
  line_total: number;
  sort_order: number;
}

export interface LineItemEdit {
  line_item_id: number;
  quantity?: number;
  unit_price?: number;
  service_description?: string;
}

export interface QuoteSummary {
  quote_id: number;
  quote_number: string;
  customer_name: string;
  status: string;
  total: number;
  quote_date: string;
}

export interface QuoteDetail {
  quote_id: number;
  quote_number: string;
  customer: Customer;
  quote_date: string;
  valid_until: string;
  status: string;
  subtotal: number;
  tax_rate: number;
  tax_amount: number;
  total: number;
  notes: string | null;
  regulatory_notes: string | null;
  line_items: LineItem[];
  created_at: string;
  updated_at: string;
}

export interface QuoteUpdate {
  notes?: string;
  regulatory_notes?: string;
  line_items?: LineItemEdit[];
}

export interface TemplateSummary {
  template_id: number;
  template_name: string;
  template_key: string;
  description: string | null;
  is_default: boolean;
  is_system: boolean;
}

export interface TemplateDetail extends TemplateSummary {
  sections: TemplateSectionConfig[];
  style_config: any;
  updated_at: string;
}

export interface TemplateSectionConfig {
  section_type: string;
  label: string;
  enabled: boolean;
  sort_order: number;
  config: any;
}
