import os
from pathlib import Path

import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
SALES_FILE = Path(os.getenv("SALES_FILE_PATH", BASE_DIR / "data" / "sales_daily.csv"))
INVENTORY_FILE = Path(
    os.getenv("INVENTORY_FILE_PATH", BASE_DIR / "data" / "inventory_daily.csv")
)


def _load_dataframe(file_path: Path) -> pd.DataFrame:
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file format: {file_path.suffix}")


def _normalize_for_json(df: pd.DataFrame) -> pd.DataFrame:
    # FastAPI/JSON cannot serialize NaN/Infinity values, so map them to null.
    normalized_df = df.replace([np.inf, -np.inf], np.nan)
    return normalized_df.where(pd.notna(normalized_df), None)


def load_sales():
    df = _load_dataframe(SALES_FILE)
    df["date"] = df["date"].astype(str)
    return _normalize_for_json(df)


def load_inventory():
    df = _load_dataframe(INVENTORY_FILE)
    df["date"] = df["date"].astype(str)
    return _normalize_for_json(df)