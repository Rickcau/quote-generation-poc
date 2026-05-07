# Quote Generation POC — Plain-Language Summary

## What Is This Project?

This is a **proof-of-concept** application for generating professional quote documents (like price estimates or proposals) for a fictitious company called **Contoso Environmental Services**. Think of it as a tool where a salesperson can pick a customer, choose a template style, tweak the details, and then download a polished PDF or Word document — all from a web browser.

The entire application runs inside **Docker containers**, so you don't need to install anything beyond Docker Desktop to try it out.

---

## How Does It Work? (The Big Picture)

The app has three main pieces that talk to each other:

1. **A web page (the UI)** — what the user sees and clicks on in their browser.
2. **A backend server (the API)** — the "brain" that processes requests, fills in templates, and builds documents.
3. **A database** — where all the customer info, quotes, and templates are stored.

```
Browser  ──▶  Web Page (Angular)  ──▶  Backend Server (Python)  ──▶  Database (SQL Server)
```

---

## Libraries & Technologies — In Plain English

### Frontend (the web page)

| Library | What It Does |
|---------|-------------|
| **Angular 17** | A framework for building interactive web pages. It handles navigation, forms, and keeping the screen in sync with data. Think of it as the construction kit for the entire user interface. |
| **Angular Material** | A set of pre-built, good-looking UI components (buttons, tables, dropdowns, dialogs) that follow Google's Material Design guidelines. Saves developers from designing every button from scratch. |
| **RxJS** | A helper library that makes it easier to deal with things that happen over time — like waiting for data to come back from the server, or reacting to a user typing in a search box. |
| **TypeScript** | A version of JavaScript with added safety checks. It catches common mistakes (like typos in variable names) before the code even runs. |
| **Nginx** | A lightweight web server that serves the web page files to your browser and forwards API requests to the backend server. Acts like a traffic cop between the browser and the backend. |

### Backend (the server / API)

| Library | What It Does |
|---------|-------------|
| **FastAPI** | A modern Python web framework for building APIs (the behind-the-scenes endpoints the web page talks to). It's fast, easy to use, and automatically generates interactive documentation. |
| **Uvicorn** | The actual server process that runs FastAPI. If FastAPI is the engine, Uvicorn is the car it sits in. |
| **Pydantic** | Validates and structures data. When the web page sends information to the server, Pydantic makes sure it's in the right shape and has the right types before anything else happens. |
| **pyodbc** | A connector that lets Python talk to SQL Server. It translates Python code into database queries so the app can read and write quote data. |
| **Jinja2** | A templating engine — think "mail merge" for documents. You write a template with placeholders like `{{customer_name}}`, and Jinja2 fills them in with real data. |
| **Markdown** | Converts simple text formatting (like `**bold**` and `# Heading`) into HTML. The quote templates are written in Markdown for simplicity, then converted for display. |
| **WeasyPrint** | Turns HTML + CSS into a PDF file. This is how the app generates downloadable PDF quotes — it renders the HTML preview as a print-quality document. |
| **python-docx** | Creates and manipulates Microsoft Word (.docx) files from Python. Used alongside **htmldocx** to convert the HTML preview into a downloadable Word document. |
| **htmldocx** | A bridge between HTML content and Word documents. It takes the HTML that was generated from the template and converts it into Word format. |

### Testing

| Library | What It Does |
|---------|-------------|
| **pytest** | The standard Python testing tool. Runs automated checks to make sure the backend code works correctly. |
| **httpx** | An HTTP client used in tests to simulate a web browser making requests to the API, so developers can verify endpoints without opening a real browser. |
| **pytest-asyncio** | Lets pytest work with Python's async features, which FastAPI uses heavily. |
| **Jasmine + Karma** | The testing tools for the Angular frontend. Jasmine defines the tests; Karma runs them in a browser behind the scenes. |

### Database

| Technology | What It Does |
|------------|-------------|
| **SQL Server 2022 (Developer Edition)** | A Microsoft relational database that stores all the customers, quotes, line items, and template configurations. The Developer Edition is free for non-production use. |

### Infrastructure / Orchestration

| Technology | What It Does |
|------------|-------------|
| **Docker** | Packages each piece of the app (database, API, UI) into its own isolated container, so it runs the same way on every machine — no "it works on my computer" problems. |
| **Docker Compose** | Lets you start all three containers with a single command (`docker-compose up`), wires them together, and makes sure they start in the right order. |

---

## In One Sentence

> This project is a Dockerized web app that lets users create, customize, preview, and download professional quote documents as PDF or Word files, powered by a Python API, an Angular frontend, and a SQL Server database.
