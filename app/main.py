from fastapi import FastAPI
from app.routes import sales, inventory

app = FastAPI(title="Sales & Inventory API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(sales.router)
app.include_router(inventory.router)