CREATE DATABASE QuotePOC;
GO
USE QuotePOC;
GO

CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    company_name NVARCHAR(200) NOT NULL,
    contact_name NVARCHAR(100),
    contact_email NVARCHAR(200),
    phone NVARCHAR(20),
    address NVARCHAR(200),
    city NVARCHAR(100),
    state NVARCHAR(2),
    zip NVARCHAR(10),
    industry NVARCHAR(100)
);

CREATE TABLE Quotes (
    quote_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL FOREIGN KEY REFERENCES Customers(customer_id),
    quote_number NVARCHAR(20) NOT NULL,
    quote_date DATE NOT NULL,
    valid_until DATE NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'Draft',
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0,
    tax_rate DECIMAL(5,4) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    total DECIMAL(12,2) NOT NULL DEFAULT 0,
    notes NVARCHAR(MAX),
    regulatory_notes NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE QuoteLineItems (
    line_item_id INT IDENTITY(1,1) PRIMARY KEY,
    quote_id INT NOT NULL FOREIGN KEY REFERENCES Quotes(quote_id),
    service_category NVARCHAR(100) NOT NULL,
    service_description NVARCHAR(500) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit NVARCHAR(20) NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL,
    sort_order INT NOT NULL DEFAULT 0
);

CREATE TABLE QuoteTemplates (
    template_id INT IDENTITY(1,1) PRIMARY KEY,
    template_name NVARCHAR(100) NOT NULL,
    template_key NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(500),
    style_config NVARCHAR(MAX),
    is_default BIT NOT NULL DEFAULT 0,
    is_system BIT NOT NULL DEFAULT 0,
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE TemplateSections (
    section_id INT IDENTITY(1,1) PRIMARY KEY,
    template_id INT NOT NULL FOREIGN KEY REFERENCES QuoteTemplates(template_id) ON DELETE CASCADE,
    section_type NVARCHAR(50) NOT NULL,
    label NVARCHAR(100) NOT NULL,
    enabled BIT NOT NULL DEFAULT 1,
    sort_order INT NOT NULL DEFAULT 0,
    config NVARCHAR(MAX)
);
GO
