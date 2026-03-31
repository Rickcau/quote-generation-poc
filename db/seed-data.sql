USE QuotePOC;
GO

-- ============================================================
-- Customers (4 records)
-- ============================================================
SET IDENTITY_INSERT Customers ON;

INSERT INTO Customers (customer_id, company_name, contact_name, contact_email, phone, address, city, state, zip, industry)
VALUES
(1, 'Apex Manufacturing', 'Sandra Kowalski', 'skowalski@apexmfg.com', '312-555-0141', '4820 Industrial Pkwy', 'Chicago', 'IL', '60638', 'Manufacturing'),
(2, 'Metro General Hospital', 'Dr. James Whitfield', 'jwhitfield@metrogenhospital.org', '713-555-0278', '9901 Medical Center Dr', 'Houston', 'TX', '77030', 'Healthcare'),
(3, 'BuildCo Construction', 'Maria Espinoza', 'mespinoza@buildcocorp.com', '720-555-0364', '3300 Commerce Blvd', 'Denver', 'CO', '80216', 'Construction'),
(4, 'Lakeside Pharmaceuticals', 'Thomas Nguyen', 'tnguyen@lakesidepharma.com', '617-555-0417', '200 Innovation Way', 'Boston', 'MA', '02210', 'Pharmaceutical');

SET IDENTITY_INSERT Customers OFF;
GO

-- ============================================================
-- Quotes (6 records)
--
-- Quote math (tax_rate = 0.0825 except where noted):
--
-- Q1 (CE-2026-0001): subtotal = 22,350.00  tax = 1843.88  total = 24,193.88
-- Q2 (CE-2026-0002): subtotal = 32,480.00  tax = 2679.60  total = 35,159.60
-- Q3 (CE-2026-0003): subtotal = 19,925.00  tax = 1643.81  total = 21,568.81
-- Q4 (CE-2026-0004): subtotal = 48,300.00  tax = 3984.75  total = 52,284.75
-- Q5 (CE-2026-0005): subtotal = 12,680.00  tax = 1046.10  total = 13,726.10
-- Q6 (CE-2026-0006): subtotal = 28,340.00  tax = 2338.05  total = 30,678.05
-- ============================================================
SET IDENTITY_INSERT Quotes ON;

INSERT INTO Quotes (quote_id, customer_id, quote_number, quote_date, valid_until, status,
                    subtotal, tax_rate, tax_amount, total, notes, regulatory_notes)
VALUES
(1, 1, 'CE-2026-0001', '2026-01-15', '2026-02-15', 'Accepted',
 22350.00, 0.0825, 1843.88, 24193.88,
 'Annual hazardous waste program for Apex Manufacturing Chicago facility. Includes scheduled pickups and emergency response retainer.',
 'All services performed in compliance with RCRA Subtitle C (40 CFR Parts 260-270) and Illinois EPA hazardous waste regulations (35 Ill. Adm. Code 700-750). Apex holds EPA ID IL0001234567. Manifest tracking required for all off-site waste shipments.'),

(2, 2, 'CE-2026-0002', '2026-01-22', '2026-02-22', 'Sent',
 32480.00, 0.0825, 2679.60, 35159.60,
 'Comprehensive medical waste and hazardous pharmaceutical disposal program for Metro General Hospital. Quarterly lab pack collections included.',
 'Medical waste disposal governed by Texas Health and Safety Code Chapter 361 and 25 TAC Chapter 326. Pharmaceutical waste managed under DEA Diversion Control regulations and EPA Universal Waste Rule (40 CFR Part 273). All manifests filed with Texas Commission on Environmental Quality (TCEQ).'),

(3, 3, 'CE-2026-0003', '2026-02-03', '2026-03-03', 'Draft',
 19925.00, 0.0825, 1643.81, 21568.81,
 'Site remediation and industrial cleaning services for BuildCo Construction downtown Denver project. Includes asbestos-containing material transport coordination.',
 'Remediation activities subject to Colorado RCRA authorization (6 CCR 1007-3) and CDPHE hazardous waste regulations. ACM transport coordinated per NESHAP standards (40 CFR Part 61, Subpart M). Site-specific Health and Safety Plan (HASP) to be provided prior to mobilization.'),

(4, 4, 'CE-2026-0004', '2026-02-10', '2026-03-10', 'Sent',
 48300.00, 0.0825, 3984.75, 52284.75,
 'Full-scope environmental services for Lakeside Pharmaceuticals Boston R&D campus. Includes controlled substance waste, solvent recovery, and annual regulatory compliance consulting package.',
 'Pharmaceutical waste disposal subject to DEA 21 CFR Part 1317 and EPA final pharmaceutical hazardous waste rule (40 CFR Parts 261, 264, 265, 266, 268, 273). Massachusetts hazardous waste regulations (310 CMR 30.000) apply. Controlled substance destruction witnessed and documented per DEA requirements. Annual compliance calendar provided as part of consulting package.'),

(5, 1, 'CE-2026-0005', '2025-10-05', '2025-11-05', 'Expired',
 12680.00, 0.0825, 1046.10, 13726.10,
 'Emergency spill response and industrial cleaning following solvent release in Building 7. Superseded by CE-2026-0001 annual program agreement.',
 'Emergency response conducted under CERCLA Section 104 notification requirements and EPCRA Section 304 emergency release notification. Illinois EPA notified within 2-hour window per 35 Ill. Adm. Code 724. Post-incident report to be submitted within 30 days of project completion.'),

(6, 3, 'CE-2026-0006', '2026-03-01', '2026-03-31', 'Draft',
 28340.00, 0.0825, 2338.05, 30678.05,
 'Soil and groundwater assessment services for BuildCo Construction eastside expansion site. Phase II ESA and remedial action planning.',
 'Phase II ESA conducted per ASTM E1903 standard. Remedial investigation subject to Colorado VCUP (Voluntary Cleanup and Redevelopment Act, C.R.S. 25-16-301). Groundwater sampling protocols per EPA Method SW-846. All laboratory analysis performed by Colorado-certified laboratories. No Further Action determination targeted upon successful remediation confirmation.');

SET IDENTITY_INSERT Quotes OFF;
GO

-- ============================================================
-- QuoteLineItems (~10 per quote, 62 total)
-- ============================================================
SET IDENTITY_INSERT QuoteLineItems ON;

-- -------------------------------------------------------
-- Quote 1 (CE-2026-0001) - Apex Manufacturing - 10 items
-- subtotal = 22,350.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(1,  1, 'Hazardous Waste Disposal',  'Drum disposal - flammable liquids (DOT Class 3), 55-gal drums',                         8.00, 'drum',   450.00,  3600.00, 10),
(2,  1, 'Hazardous Waste Disposal',  'Drum disposal - corrosive liquids (DOT Class 8), 55-gal drums',                          6.00, 'drum',   420.00,  2520.00, 20),
(3,  1, 'Hazardous Waste Disposal',  'Bulk liquid waste transport and disposal, non-halogenated solvents',                     2.00, 'ton',   1250.00,  2500.00, 30),
(4,  1, 'Hazardous Waste Disposal',  'Small container consolidation and disposal (< 5 gallon containers)',                    40.00, 'each',    85.00,  3400.00, 40),
(5,  1, 'Emergency Spill Response',  'Emergency response retainer - 4-hour guaranteed response, monthly',                    12.00, 'month',  350.00,  4200.00, 50),
(6,  1, 'Industrial Cleaning',       'Industrial vacuum truck service, holding tank cleanout',                                 2.00, 'event',  950.00,  1900.00, 60),
(7,  1, 'Industrial Cleaning',       'Pressure washing and decontamination, drum storage area (1000 sq ft)',                   2.00, 'event',  480.00,   960.00, 70),
(8,  1, 'Lab Pack Services',         'Lab pack collection and characterization, mixed organic waste',                          1.00, 'event', 1200.00,  1200.00, 80),
(9,  1, 'Regulatory Consulting',     'Annual hazardous waste generator status review and reporting assistance',                1.00, 'year',  1200.00,  1200.00, 90),
(10, 1, 'Regulatory Consulting',     'RCRA training - 8-hour annual refresher, up to 15 employees',                           1.00, 'event',  870.00,   870.00, 100);

-- -------------------------------------------------------
-- Quote 2 (CE-2026-0002) - Metro General Hospital - 11 items
-- subtotal = 31,480.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(11, 2, 'Hazardous Waste Disposal',  'Pharmaceutical waste disposal - non-controlled, bulk containers',                        4.00, 'drum',   510.00,  2040.00, 10),
(12, 2, 'Hazardous Waste Disposal',  'Chemotherapy waste disposal, segregated sharps and trace-contaminated materials',        6.00, 'box',    320.00,  1920.00, 20),
(13, 2, 'Hazardous Waste Disposal',  'P-listed acute hazardous pharmaceutical waste, lab-pack format',                         1.00, 'event', 2400.00,  2400.00, 30),
(14, 2, 'Hazardous Waste Disposal',  'Mercury-containing device disposal (thermometers, sphygmomanometers)',                  80.00, 'each',    28.00,  2240.00, 40),
(15, 2, 'Lab Pack Services',         'Quarterly lab pack - radiology and pathology chemical waste',                            4.00, 'event', 1850.00,  7400.00, 50),
(16, 2, 'Lab Pack Services',         'Lab pack collection - fixatives and staining reagents (formaldehyde-based)',             2.00, 'event', 1650.00,  3300.00, 60),
(17, 2, 'Industrial Cleaning',       'Fume hood decontamination and wipe-down, pharmacy compounding area',                    3.00, 'event',  740.00,  2220.00, 70),
(18, 2, 'Industrial Cleaning',       'Spill kit replenishment and biohazard area deep clean, per wing',                       4.00, 'event',  560.00,  2240.00, 80),
(19, 2, 'Regulatory Consulting',     'Joint Commission environmental compliance gap assessment',                               1.00, 'event', 3200.00,  3200.00, 90),
(20, 2, 'Regulatory Consulting',     'RCRA/TCEQ annual report preparation and submission support',                            1.00, 'year',  1580.00,  1580.00, 100),
(21, 2, 'Regulatory Consulting',     'DEA controlled substance waste disposal witnessing and documentation',                   4.00, 'event',  985.00,  3940.00, 110);

-- -------------------------------------------------------
-- Quote 3 (CE-2026-0003) - BuildCo Construction - 10 items
-- subtotal = 18,925.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(22, 3, 'Hazardous Waste Disposal',  'Asbestos-containing material (ACM) transport and disposal, friable',                    3.00, 'ton',   1800.00,  5400.00, 10),
(23, 3, 'Hazardous Waste Disposal',  'Lead-based paint waste disposal, debris and chip containers',                           5.00, 'drum',   390.00,  1950.00, 20),
(24, 3, 'Hazardous Waste Disposal',  'Petroleum-impacted soil disposal, rolloff container service',                           8.00, 'ton',    275.00,  2200.00, 30),
(25, 3, 'Industrial Cleaning',       'High-pressure wash down and vacuum recovery, contaminated slabs',                       4.00, 'event',  620.00,  2480.00, 40),
(26, 3, 'Industrial Cleaning',       'Decontamination trailer setup and operations (per day)',                                 5.00, 'day',    380.00,  1900.00, 50),
(27, 3, 'Emergency Spill Response',  'Spill containment boom deployment and product recovery, fuel release',                  1.00, 'event', 2150.00,  2150.00, 60),
(28, 3, 'Lab Pack Services',         'Lab pack - paint-related waste, thinners and used solvents',                            1.00, 'event',  975.00,   975.00, 70),
(29, 3, 'Regulatory Consulting',     'Site-specific HASP development (Health and Safety Plan)',                               1.00, 'each',   870.00,   870.00, 80),
(30, 3, 'Regulatory Consulting',     'CDPHE permit application preparation for temporary waste accumulation area',            1.00, 'each',   650.00,   650.00, 90),
(31, 3, 'Regulatory Consulting',     'Field technician oversight and daily compliance monitoring (per day)',                   5.00, 'day',    270.00,  1350.00, 100);

-- -------------------------------------------------------
-- Quote 4 (CE-2026-0004) - Lakeside Pharmaceuticals - 11 items
-- subtotal = 44,750.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(32, 4, 'Hazardous Waste Disposal',  'Solvent waste disposal - halogenated solvents (DCM, chloroform), drum',                 10.00, 'drum',   580.00,  5800.00, 10),
(33, 4, 'Hazardous Waste Disposal',  'Solvent waste disposal - non-halogenated solvents (acetonitrile, methanol)',            10.00, 'drum',   460.00,  4600.00, 20),
(34, 4, 'Hazardous Waste Disposal',  'Reactive and oxidizer waste disposal (peroxide-forming chemicals)',                     2.00, 'drum',   950.00,  1900.00, 30),
(35, 4, 'Hazardous Waste Disposal',  'Bulk liquid waste - aqueous with heavy metals, neutralization and disposal',            4.00, 'ton',   1350.00,  5400.00, 40),
(36, 4, 'Lab Pack Services',         'Comprehensive lab pack - R&D bench chemicals, full characterization',                   4.00, 'event', 2200.00,  8800.00, 50),
(37, 4, 'Lab Pack Services',         'Lab pack - expired reference standards and reagents, analytical grade',                 2.00, 'event', 1750.00,  3500.00, 60),
(38, 4, 'Hazardous Waste Disposal',  'DEA Schedule II-V controlled substance waste disposal, witnessed destruction',          4.00, 'event', 1850.00,  7400.00, 70),
(39, 4, 'Industrial Cleaning',       'Cleanroom decontamination and HEPA vacuuming, ISO Class 7 suite',                       2.00, 'event', 1600.00,  3200.00, 80),
(40, 4, 'Regulatory Consulting',     'Annual EPA/DEA compliance audit and corrective action plan',                            1.00, 'year',  4200.00,  4200.00, 90),
(41, 4, 'Regulatory Consulting',     'Massachusetts 310 CMR 30.000 annual report preparation',                               1.00, 'year',  1850.00,  1850.00, 100),
(42, 4, 'Regulatory Consulting',     'Waste minimization program development and documentation',                              1.00, 'event', 1650.00,  1650.00, 110);

-- -------------------------------------------------------
-- Quote 5 (CE-2026-0005) - Apex Manufacturing (Expired) - 10 items
-- subtotal = 12,680.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(43, 5, 'Emergency Spill Response',  'Emergency mobilization fee - 2-hour response, Building 7 solvent release',              1.00, 'event', 2500.00,  2500.00, 10),
(44, 5, 'Emergency Spill Response',  'Spill containment and product recovery, non-halogenated solvent',                       1.00, 'event', 1800.00,  1800.00, 20),
(45, 5, 'Emergency Spill Response',  'Emergency air monitoring - PID/photoionization detection, per day',                     3.00, 'day',    450.00,  1350.00, 30),
(46, 5, 'Emergency Spill Response',  'PPE - Level B protection, per responder per day (4 responders x 2 days)',               8.00, 'each',   280.00,  2240.00, 40),
(47, 5, 'Industrial Cleaning',       'Absorbent media application, recovery, and containerization',                           1.00, 'event',  920.00,   920.00, 50),
(48, 5, 'Industrial Cleaning',       'Industrial vacuum truck, contaminated wash water recovery',                             1.00, 'event',  850.00,   850.00, 60),
(49, 5, 'Hazardous Waste Disposal',  'Drum disposal - contaminated absorbents and PPE, per drum',                             4.00, 'drum',   390.00,  1560.00, 70),
(50, 5, 'Hazardous Waste Disposal',  'Contaminated wash water disposal, aqueous waste',                                       1.00, 'ton',    460.00,   460.00, 80),
(51, 5, 'Regulatory Consulting',     'EPCRA Section 304 release notification report preparation',                             1.00, 'event',  650.00,   650.00, 90),
(52, 5, 'Regulatory Consulting',     'Post-incident investigation and 30-day compliance report',                              1.00, 'event',  350.00,   350.00, 100);

-- -------------------------------------------------------
-- Quote 6 (CE-2026-0006) - BuildCo Construction - 10 items
-- subtotal = 27,340.00
-- -------------------------------------------------------
INSERT INTO QuoteLineItems (line_item_id, quote_id, service_category, service_description, quantity, unit, unit_price, line_total, sort_order)
VALUES
(53, 6, 'Hazardous Waste Disposal',  'Petroleum-impacted soil excavation and off-site disposal',                             15.00, 'ton',    340.00,  5100.00, 10),
(54, 6, 'Hazardous Waste Disposal',  'Free-phase product recovery (petroleum), drum containerization',                        3.00, 'drum',   430.00,  1290.00, 20),
(55, 6, 'Industrial Cleaning',       'Heavy equipment decontamination, excavators and loader (per unit)',                     3.00, 'each',   580.00,  1740.00, 30),
(56, 6, 'Industrial Cleaning',       'Groundwater treatment system O&M, air stripper (per month)',                            3.00, 'month', 1200.00,  3600.00, 40),
(57, 6, 'Industrial Cleaning',       'Injection well installation, oxygen-releasing compound (ORC), per well',                4.00, 'each',  1450.00,  5800.00, 50),
(58, 6, 'Emergency Spill Response',  'Standby emergency response coverage during active excavation (per day)',                5.00, 'day',    480.00,  2400.00, 60),
(59, 6, 'Lab Pack Services',         'Soil and groundwater sampling, Phase II ESA grid (20 locations)',                       1.00, 'event', 3200.00,  3200.00, 70),
(60, 6, 'Regulatory Consulting',     'Remedial action plan (RAP) development and CDPHE submission',                           1.00, 'event', 2800.00,  2800.00, 80),
(61, 6, 'Regulatory Consulting',     'VCUP enrollment assistance and NFA petition preparation',                               1.00, 'event',  760.00,   760.00, 90),
(62, 6, 'Regulatory Consulting',     'Quarterly groundwater monitoring report preparation and submittal',                     2.00, 'event',  825.00,  1650.00, 100);

SET IDENTITY_INSERT QuoteLineItems OFF;
GO

-- ============================================================
-- QuoteTemplates (3 system templates)
-- ============================================================
SET IDENTITY_INSERT QuoteTemplates ON;

INSERT INTO QuoteTemplates (template_id, template_name, template_key, description, style_config, is_default, is_system, updated_at)
VALUES
(1,
 'Formal Detailed',
 'formal',
 'Full-detail formal proposal format with cover page, itemized line items, regulatory notes, terms, and signature block. Best for large accounts and regulated industries.',
 '{"fontFamily":"Calibri","fontSize":11,"primaryColor":"#1a3a5c","accentColor":"#2e7d32","logoPosition":"top-left","pageSize":"letter","margins":{"top":1.0,"bottom":1.0,"left":1.25,"right":1.25},"showPageNumbers":true,"headerStyle":"full"}',
 1, 1, SYSUTCDATETIME()),

(2,
 'Summary',
 'summary',
 'Concise single-page summary format showing totals and key service categories. Suitable for renewal quotes and existing customers who do not require full detail.',
 '{"fontFamily":"Arial","fontSize":10,"primaryColor":"#333333","accentColor":"#0072c6","logoPosition":"top-right","pageSize":"letter","margins":{"top":0.75,"bottom":0.75,"left":1.0,"right":1.0},"showPageNumbers":false,"headerStyle":"minimal"}',
 0, 1, SYSUTCDATETIME()),

(3,
 'Branded Proposal',
 'proposal',
 'Premium branded proposal with full corporate styling, executive summary narrative, categorized services, compliance highlights, and custom cover page. Ideal for new enterprise prospects.',
 '{"fontFamily":"Georgia","fontSize":11,"primaryColor":"#0d3349","accentColor":"#e65100","logoPosition":"center","pageSize":"letter","margins":{"top":1.0,"bottom":1.0,"left":1.25,"right":1.25},"showPageNumbers":true,"headerStyle":"branded","coverPage":true,"executiveSummary":true}',
 0, 1, SYSUTCDATETIME());

SET IDENTITY_INSERT QuoteTemplates OFF;
GO

-- ============================================================
-- TemplateSections (6 section types x 3 templates = 18 records)
-- ============================================================
SET IDENTITY_INSERT TemplateSections ON;

-- Template 1: Formal Detailed
INSERT INTO TemplateSections (section_id, template_id, section_type, label, enabled, sort_order, config)
VALUES
(1,  1, 'header',     'Document Header',       1, 10, '{"showLogo":true,"showQuoteNumber":true,"showDate":true,"showCustomerAddress":true,"showValidUntil":true}'),
(2,  1, 'summary',    'Quote Summary',          1, 20, '{"showSubtotal":true,"showTaxRate":true,"showTaxAmount":true,"showTotal":true,"showStatus":true,"highlightTotal":true}'),
(3,  1, 'line_items', 'Service Line Items',     1, 30, '{"groupByCategory":true,"showUnitPrice":true,"showQuantity":true,"showUnit":true,"showLineTotal":true,"showSortOrder":false}'),
(4,  1, 'regulatory', 'Regulatory Notes',       1, 40, '{"showRegulationCitations":true,"boxStyle":"bordered","iconStyle":"warning","fontSize":10}'),
(5,  1, 'terms',      'Terms and Conditions',  1, 50, '{"termsVersion":"v2.3","showPaymentTerms":true,"paymentDays":30,"showCancellationPolicy":true,"showLiabilityClause":true}'),
(6,  1, 'signature',  'Signature Block',        1, 60, '{"requireCustomerSignature":true,"requireDateLine":true,"showPrintedName":true,"showTitleLine":true,"showWitnessLine":false}'),

-- Template 2: Summary
(7,  2, 'header',     'Document Header',        1, 10, '{"showLogo":true,"showQuoteNumber":true,"showDate":true,"showCustomerAddress":false,"showValidUntil":true}'),
(8,  2, 'summary',    'Quote Summary',           1, 20, '{"showSubtotal":true,"showTaxRate":false,"showTaxAmount":false,"showTotal":true,"showStatus":true,"highlightTotal":true}'),
(9,  2, 'line_items', 'Services Summary',        1, 30, '{"groupByCategory":true,"showUnitPrice":false,"showQuantity":false,"showUnit":false,"showLineTotal":true,"showSortOrder":false,"collapsedView":true}'),
(10, 2, 'regulatory', 'Regulatory Notes',        0, 40, '{"showRegulationCitations":false,"boxStyle":"simple","iconStyle":"none","fontSize":9}'),
(11, 2, 'terms',      'Terms and Conditions',   1, 50, '{"termsVersion":"v2.3","showPaymentTerms":true,"paymentDays":30,"showCancellationPolicy":false,"showLiabilityClause":false}'),
(12, 2, 'signature',  'Signature Block',         1, 60, '{"requireCustomerSignature":true,"requireDateLine":true,"showPrintedName":false,"showTitleLine":false,"showWitnessLine":false}'),

-- Template 3: Branded Proposal
(13, 3, 'header',     'Executive Cover',         1, 10, '{"showLogo":true,"showQuoteNumber":true,"showDate":true,"showCustomerAddress":true,"showValidUntil":true,"showTagline":true,"coverPageTitle":"Environmental Services Proposal","tagline":"Committed to Compliance. Committed to You."}'),
(14, 3, 'summary',    'Investment Summary',      1, 20, '{"showSubtotal":true,"showTaxRate":true,"showTaxAmount":true,"showTotal":true,"showStatus":true,"highlightTotal":true,"executiveSummaryNarrative":true}'),
(15, 3, 'line_items', 'Scope of Services',       1, 30, '{"groupByCategory":true,"showUnitPrice":true,"showQuantity":true,"showUnit":true,"showLineTotal":true,"showSortOrder":false,"categoryDescriptions":true,"showCategoryIcons":true}'),
(16, 3, 'regulatory', 'Compliance Framework',    1, 40, '{"showRegulationCitations":true,"boxStyle":"shaded","iconStyle":"shield","fontSize":10,"showComplianceMatrix":true}'),
(17, 3, 'terms',      'Terms and Conditions',   1, 50, '{"termsVersion":"v2.3","showPaymentTerms":true,"paymentDays":30,"showCancellationPolicy":true,"showLiabilityClause":true,"showInsuranceCertification":true}'),
(18, 3, 'signature',  'Authorization Block',     1, 60, '{"requireCustomerSignature":true,"requireDateLine":true,"showPrintedName":true,"showTitleLine":true,"showWitnessLine":true,"showNotaryBlock":false}');

SET IDENTITY_INSERT TemplateSections OFF;
GO
