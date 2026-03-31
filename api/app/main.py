from fastapi import FastAPI
from app.database import check_health

app = FastAPI(title="Quote Generation POC", version="1.0.0")

@app.get("/api/health")
def health():
    db_ok = check_health()
    return {"status": "healthy" if db_ok else "unhealthy", "database": db_ok}
