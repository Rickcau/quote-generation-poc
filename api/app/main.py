from fastapi import FastAPI
from app.database import check_health
from app.routers import quotes, customers

app = FastAPI(title="Quote Generation POC", version="1.0.0")

app.include_router(quotes.router)
app.include_router(customers.router)

@app.get("/api/health")
def health():
    db_ok = check_health()
    return {"status": "healthy" if db_ok else "unhealthy", "database": db_ok}
