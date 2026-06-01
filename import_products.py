from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parent
DEFAULT_CSV = ROOT / "data" / "products.csv"


def load_products(path: Path = DEFAULT_CSV) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).fillna("")
    required = [
        "barcode",
        "last6",
        "product_name",
        "brand",
        "status",
        "msl",
        "max_qty",
        "stc_planogram_location",
        "brossard_planogram_location",
        "st_laurent_planogram_location",
    ]
    missing = [col for col in required if col not in df.columns]
    for col in missing:
        df[col] = ""
    df["barcode"] = df["barcode"].str.replace(r"\D", "", regex=True)
    df["last6"] = df["barcode"].str[-6:]
    return df[required].drop_duplicates("barcode")


def import_to_supabase() -> None:
    from supabase import create_client

    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    client = create_client(url, key)

    df = load_products()
    rows = df.to_dict("records")
    batch_size = 500
    for start in range(0, len(rows), batch_size):
        client.table("products").upsert(rows[start : start + batch_size], on_conflict="barcode").execute()
    print(f"Imported {len(rows)} products.")


if __name__ == "__main__":
    import_to_supabase()
