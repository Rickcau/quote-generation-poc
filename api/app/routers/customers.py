from fastapi import APIRouter
from app.database import fetch_all
from app.models import Customer

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("/", response_model=list[Customer])
def list_customers():
    return fetch_all("SELECT * FROM Customers ORDER BY company_name")
