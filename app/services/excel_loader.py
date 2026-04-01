import os
from pathlib import Path

import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
SALES_FILE = Path(os.getenv("SALES_FILE_PATH", BASE_DIR / "data" / "raw_sales.csv"))
INVENTORY_FILE = Path(
    os.getenv("INVENTORY_FILE_PATH", BASE_DIR / "data" / "raw_inventory.csv")
)


def _load_dataframe(file_path: Path) -> pd.DataFrame:
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file format: {file_path.suffix}")


def _normalize_for_json(df: pd.DataFrame) -> pd.DataFrame:
    # FastAPI/JSON cannot serialize NaN/Infinity values, so map them to null.
    normalized_df = df.copy()
    numeric_columns = normalized_df.select_dtypes(include=[np.number]).columns
    normalized_df[numeric_columns] = normalized_df[numeric_columns].replace(
        [np.inf, -np.inf], np.nan
    )
    return normalized_df.astype(object).where(pd.notna(normalized_df), None)


def _ensure_date_column(df: pd.DataFrame, candidate_columns: list[str]) -> pd.DataFrame:
    if "date" in df.columns:
        date_series = pd.to_datetime(df["date"], errors="coerce")
    else:
        source_column = next((column for column in candidate_columns if column in df.columns), None)
        if source_column is None:
            raise ValueError(
                "Missing date source. Expected one of: "
                + ", ".join(["date"] + candidate_columns)
            )
        date_series = pd.to_datetime(df[source_column], errors="coerce")

    df["date"] = date_series.dt.strftime("%Y-%m-%d")
    return df


def load_sales():
    df = _load_dataframe(SALES_FILE)
    df = _ensure_date_column(df, ["transaction_datetime", "event_timestamp"])
    return _normalize_for_json(df)


def load_inventory():
    df = _load_dataframe(INVENTORY_FILE)
    df = _ensure_date_column(df, ["event_timestamp", "transaction_datetime"])
    return _normalize_for_json(df)