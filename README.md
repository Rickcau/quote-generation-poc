# Quote Document Generation POC

**Author:** Rick Caudle
**Company (fictitious):** Contoso Environmental Services

A self-contained Docker Compose proof-of-concept demonstrating a modern Python-based quote document generation architecture. The system pulls quote data from SQL Server, renders it through Jinja2/Markdown templates, and generates PDF, DOCX, and HTML output — all managed through an Angular UI.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v4.x or later)
- Docker Compose v2 (bundled with Docker Desktop)
- At least 4 GB of RAM allocated to Docker (SQL Server requirement)

No other local tooling required — all runtimes run inside containers.

---

## Quickstart

```bash
cd quote-generation-poc
docker-compose up --build
```

First build takes several minutes. Subsequent starts are faster.

```bash
# Stop the stack
docker-compose down

# Stop and reset database (full reset)
docker-compose down -v
```

---

## Service URLs

| Service | URL |
|---------|-----|
| Angular UI | http://localhost:4200 |
| FastAPI REST API | http://localhost:8000 |
| Swagger / OpenAPI Docs | http://localhost:8000/docs |

---

## Demo Walkthrough

1. Open http://localhost:4200 — see the **Quote List** with 6 sample quotes
2. Click a quote — see the **Quote Preview** with rendered HTML
3. Switch templates using the **Template** dropdown (Formal, Summary, Proposal)
4. Click **Edit** — modify notes, regulatory text, or line item quantities/prices
5. Click **Save** — changes persist to the database, preview updates
6. Click **PDF** or **DOCX** — download the generated document
7. Navigate to **Template Builder** — configure custom templates
8. Toggle sections on/off, reorder them, change color scheme and font
9. Click **Save Template** — new template appears in the template selector

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Angular UI (Nginx)         localhost:4200   │
└──────────────────┬──────────────────────────┘
                   │ HTTP (JSON) via Nginx proxy
┌──────────────────▼──────────────────────────┐
│  Python API (FastAPI)       localhost:8000   │
│                                              │
│  ├── Data Access Layer (pyodbc)              │
│  ├── Template Engine (Jinja2 + Markdown)     │
│  ├── Template Compiler (section-based)       │
│  └── Document Renderers (HTML/PDF/DOCX)      │
└──────────────────┬──────────────────────────┘
                   │ pyodbc (ODBC Driver 18)
┌──────────────────▼──────────────────────────┐
│  SQL Server 2022 Developer  localhost:1433   │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
quote-generation-poc/
├── docker-compose.yml
├── db/
│   ├── Dockerfile
│   ├── entrypoint.sh           # Auto-init on first boot
│   ├── init-schema.sql         # 5 tables
│   └── seed-data.sql           # 4 customers, 6 quotes, ~60 line items, 3 templates
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI app with health endpoint
│   │   ├── config.py           # DB connection config (env vars)
│   │   ├── database.py         # SQL connection layer
│   │   ├── models.py           # Pydantic models
│   │   ├── template_compiler.py # Section config → Jinja2/Markdown
│   │   ├── routers/
│   │   │   ├── quotes.py       # GET/PUT quotes, GET customers
│   │   │   ├── templates.py    # CRUD templates + preview
│   │   │   ├── documents.py    # Preview (HTML) + Render (PDF/DOCX)
│   │   │   └── customers.py    # GET customers
│   │   ├── templates/          # Jinja2/Markdown templates
│   │   │   ├── formal.md.j2
│   │   │   ├── summary.md.j2
│   │   │   ├── proposal.md.j2
│   │   │   └── sections/       # 6 reusable building blocks
│   │   └── renderers/
│   │       ├── html_renderer.py
│   │       ├── pdf_renderer.py
│   │       └── docx_renderer.py
│   └── tests/
└── ui/
    ├── Dockerfile
    ├── nginx.conf              # Proxies /api/* to FastAPI
    └── src/app/
        ├── components/
        │   ├── quote-list/         # Sortable Material table
        │   ├── quote-preview/      # HTML preview + PDF/DOCX download
        │   ├── quote-editor/       # Edit notes + line items
        │   ├── template-selector/  # Template dropdown
        │   └── template-builder/   # Section config + style picker
        ├── services/api.service.ts
        └── models/quote.model.ts
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Database | SQL Server 2022 Developer (Docker) |
| API | Python 3.12, FastAPI, pyodbc |
| Templating | Jinja2 + Markdown |
| PDF Generation | WeasyPrint (CSS-based) |
| DOCX Generation | htmldocx + python-docx |
| Frontend | Angular 17, Angular Material |
| Web Server | Nginx (proxies API, serves SPA) |
| Orchestration | Docker Compose |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/quotes | List all quotes |
| GET | /api/quotes/{id} | Quote detail with line items |
| PUT | /api/quotes/{id} | Update quote |
| GET | /api/customers | List customers |
| GET | /api/templates | List templates |
| GET | /api/templates/{id} | Template detail with sections |
| POST | /api/templates | Create template |
| PUT | /api/templates/{id} | Update template |
| DELETE | /api/templates/{id} | Delete template |
| POST | /api/templates/preview | Preview template with sample data |
| POST | /api/documents/preview | Render quote as HTML |
| POST | /api/documents/render | Generate PDF or DOCX |

---

## Default Credentials

| Item | Value |
|------|-------|
| SQL Server SA password | `QuotePOC!2026` |
| Database name | `QuotePOC` |

Development-only credentials. Do not use in production.

---

## Sample Data

- **4 customers:** Apex Manufacturing, Metro General Hospital, BuildCo Construction, Lakeside Pharmaceuticals
- **6 quotes:** Various statuses (Draft, Sent, Accepted, Expired)
- **~60 line items:** Hazardous Waste Disposal, Emergency Spill Response, Industrial Cleaning, Lab Pack Services, Regulatory Consulting
- **3 system templates:** Formal Detailed, Summary, Branded Proposal
