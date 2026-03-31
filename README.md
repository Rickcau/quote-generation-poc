# Quote Document Generation POC

**Author:** Rick Caudle
**Company (fictitious):** Contoso Environmental Services

A self-contained, Docker Compose-based proof of concept demonstrating automated quote document generation for environmental services. The system accepts job and pricing data through an Angular UI, persists it in SQL Server, and generates formatted quote documents via a Python/FastAPI backend.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v4.x or later)
- Docker Compose v2 (bundled with Docker Desktop)
- At least 4 GB of RAM allocated to Docker (SQL Server requirement)

No other local tooling is required — all runtimes (Python, Node, SQL Server) run inside containers.

---

## Quickstart

```bash
# Clone the repo (or unzip the project folder)
cd quote-generation-poc

# Build all images and start the stack
docker-compose up --build
```

First build takes several minutes while Docker pulls base images and installs dependencies. Subsequent starts are much faster.

To stop the stack:

```bash
docker-compose down
```

To stop and remove the database volume (full reset):

```bash
docker-compose down -v
```

---

## Service URLs

| Service | URL |
|---|---|
| Angular UI | http://localhost:4200 |
| FastAPI (REST) | http://localhost:8000 |
| Swagger / OpenAPI Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## Project Structure

```
quote-generation-poc/
├── docker-compose.yml      # Orchestrates all three services
├── .gitignore
├── README.md
│
├── db/                     # SQL Server 2022 container
│   ├── Dockerfile
│   └── init/               # SQL init scripts (schema + seed data)
│
├── api/                    # Python / FastAPI container
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── routers/        # API route handlers
│       ├── models/         # SQLAlchemy ORM models
│       ├── schemas/        # Pydantic request/response schemas
│       └── services/       # Business logic, document generation
│
└── ui/                     # Angular application container (served via nginx)
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        └── app/
            ├── components/ # Reusable UI components
            └── pages/      # Quote list, quote editor, preview
```

---

## What This POC Demonstrates

Contoso Environmental Services handles dozens of customer quotes per week for waste remediation, hazardous material transport, and site cleanup jobs. This POC validates a modernized quoting workflow:

1. **Data entry** — A dispatcher fills out a quote form in the Angular UI, selecting services, quantities, and customer details.
2. **Persistence** — Quote data is stored in a SQL Server 2022 database with a normalized schema (customers, quotes, line items, services catalog).
3. **Document generation** — The FastAPI backend assembles a formatted quote document (PDF/DOCX) from a template, populated with the stored data.
4. **Review & download** — The completed document is previewed in the UI and available for download or email.

Key technical decisions validated by this POC:
- SQL Server on Linux in Docker as a cost-effective dev/test database
- FastAPI for rapid API development with automatic OpenAPI documentation
- Angular standalone components for a maintainable, typed front end
- Docker Compose for a zero-install local development and demo environment

---

## Default Credentials

| Item | Value |
|---|---|
| SQL Server SA password | `QuotePOC!2026` |
| Database name | `QuotePOC` |

These are development-only credentials hard-coded for convenience. Do not use in production.
