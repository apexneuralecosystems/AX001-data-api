from fastapi import APIRouter, Query
from app.services.excel_loader import load_inventory

router = APIRouter()

# /inventory?date=2023-02-20
@router.get("/inventory")
def get_inventory_by_date(date: str = Query(...)):
    df = load_inventory()
    result = df[df['date'] == date]
    return result.to_dict(orient="records")


# /inventory/all
@router.get("/inventory/all")
def get_all_inventory():
    df = load_inventory()
    return df.to_dict(orient="records")