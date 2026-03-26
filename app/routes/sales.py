from fastapi import APIRouter, Query
from app.services.excel_loader import load_sales

router = APIRouter()

# /sales?date=2023-02-20
@router.get("/sales")
def get_sales_by_date(date: str = Query(...)):
    df = load_sales()
    result = df[df['date'] == date]
    return result.to_dict(orient="records")


# /sales/all
@router.get("/sales/all")
def get_all_sales():
    df = load_sales()
    return df.to_dict(orient="records")