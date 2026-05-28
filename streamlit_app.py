from __future__ import annotations

from datetime import date
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
PRODUCT_CSV = ROOT / "data" / "products.csv"
LOCAL_RECORDS_CSV = ROOT / "data" / "records_local.csv"
REPORT_LABELS = {
    "tester": "Tester",
    "damage": "Damage",
    "theft": "Theft",
    "restock": "Restock",
}


st.set_page_config(page_title="BA Consignment System", layout="wide")


def secret_value(name: str, default=None):
    try:
        return st.secrets[name]
    except Exception:
        return default


def use_supabase() -> bool:
    return bool(secret_value("USE_SUPABASE", False)) and bool(secret_value("SUPABASE_URL")) and bool(secret_value("SUPABASE_KEY"))


@st.cache_resource(show_spinner=False)
def supabase_client():
    from supabase import create_client

    return create_client(secret_value("SUPABASE_URL"), secret_value("SUPABASE_KEY"))


@st.cache_data(ttl=300, show_spinner=False)
def load_products() -> pd.DataFrame:
    if use_supabase():
        response = supabase_client().table("products").select("*").execute()
        df = pd.DataFrame(response.data)
    else:
        df = pd.read_csv(PRODUCT_CSV, dtype=str)

    if df.empty:
        return pd.DataFrame(columns=["barcode", "last6", "product_name", "brand", "category", "status", "msl", "max_qty"])

    for col in ["barcode", "last6", "product_name", "brand", "category", "status", "msl", "max_qty"]:
        if col not in df.columns:
            df[col] = ""
    df = df.fillna("")
    df["barcode"] = df["barcode"].astype(str)
    df["last6"] = df["barcode"].str[-6:]
    return df[["barcode", "last6", "product_name", "brand", "category", "status", "msl", "max_qty"]]


def load_records() -> pd.DataFrame:
    columns = [
        "id",
        "report_type",
        "report_date",
        "ba_name",
        "store_name",
        "input_code",
        "qty",
        "barcode",
        "product_name",
        "brand",
        "category",
        "notes",
        "created_at",
    ]

    if use_supabase():
        response = supabase_client().table("records").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data, columns=columns)

    if LOCAL_RECORDS_CSV.exists():
        return pd.read_csv(LOCAL_RECORDS_CSV, dtype=str).fillna("")
    return pd.DataFrame(columns=columns)


def save_record(record: dict) -> None:
    if use_supabase():
        supabase_client().table("records").insert(record).execute()
        return

    records = load_records()
    records = pd.concat([pd.DataFrame([record]), records], ignore_index=True)
    records.to_csv(LOCAL_RECORDS_CSV, index=False, encoding="utf-8-sig")


def normalize_code(value: str) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def find_products(products: pd.DataFrame, code: str) -> pd.DataFrame:
    clean = normalize_code(code)
    if not clean:
        return products.iloc[0:0]
    if len(clean) > 6:
        exact = products[products["barcode"] == clean]
        if not exact.empty:
            return exact
    last6 = clean[-6:]
    return products[(products["last6"] == last6) | (products["barcode"].str.endswith(last6, na=False))]


def get_users() -> dict:
    try:
        return dict(st.secrets["users"])
    except Exception:
        return {
            "admin": {"password": "admin123", "role": "admin", "display_name": "Admin User"},
            "ba": {"password": "ba123", "role": "ba", "display_name": "BA User", "store_name": "Miniso Test Store"},
        }


def login_screen() -> None:
    st.title("BA Consignment Store System")
    st.caption("Sign in with a BA or Admin account.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)

    if submitted:
        users = get_users()
        user = users.get(username.strip().lower())
        if not user or user.get("password") != password:
            st.error("Username or password is incorrect.")
            return
        st.session_state.user = {
            "username": username.strip().lower(),
            "role": user.get("role", "ba"),
            "display_name": user.get("display_name", username),
            "store_name": user.get("store_name", ""),
        }
        st.rerun()

    st.info("Demo BA: ba / ba123\n\nDemo Admin: admin / admin123")


def logout_button() -> None:
    user = st.session_state.user
    st.sidebar.write(f"Signed in as **{user['display_name']}**")
    st.sidebar.caption(f"Role: {user['role'].upper()}")
    if st.sidebar.button("Sign out", use_container_width=True):
        del st.session_state.user
        st.rerun()


def search_page(products: pd.DataFrame) -> None:
    st.header("Product Search")
    col1, col2 = st.columns([3, 1])
    query = col1.text_input("Search by keyword, barcode, last 6, brand, or category")
    categories = ["All"] + sorted([c for c in products["category"].dropna().unique().tolist() if c])
    category = col2.selectbox("Category", categories)

    filtered = products.copy()
    if category != "All":
        filtered = filtered[filtered["category"] == category]
    if query.strip():
        q = query.strip().lower()
        haystack = filtered[["barcode", "last6", "product_name", "brand", "category", "status"]].agg(" ".join, axis=1).str.lower()
        filtered = filtered[haystack.str.contains(q, na=False)]

    st.caption(f"{len(filtered)} matching products")
    st.dataframe(
        filtered[["barcode", "last6", "product_name", "brand", "category", "status"]],
        hide_index=True,
        use_container_width=True,
    )


def record_page(products: pd.DataFrame) -> None:
    st.header("BA Record")
    user = st.session_state.user

    with st.form("record_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        report_type = col1.selectbox("Type", list(REPORT_LABELS.keys()), format_func=lambda key: REPORT_LABELS[key])
        report_date = col2.date_input("Date", value=date.today())
        qty = col3.number_input("Qty", min_value=1, value=1, step=1)

        col4, col5 = st.columns(2)
        ba_name = col4.text_input("BA name", value=user["display_name"])
        store_name = col5.text_input("Store", value=user.get("store_name", ""))

        code = st.text_input("Scan barcode or enter last 6")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save record", use_container_width=True)

    matches = find_products(products, code)
    selected_product = None
    if code:
        if matches.empty:
            st.warning("No product found for this barcode / last 6.")
        else:
            options = matches["barcode"].tolist()
            selected_barcode = st.selectbox(
                "Product match",
                options,
                format_func=lambda barcode: matches.loc[matches["barcode"] == barcode, "product_name"].iloc[0],
            )
            selected_product = matches[matches["barcode"] == selected_barcode].iloc[0].to_dict()
            st.success(f"{selected_product['barcode']} | {selected_product['product_name']} | {selected_product['brand']}")

    if submitted:
        if not selected_product:
            st.error("Please enter a valid product barcode or last 6 before saving.")
            return
        record = {
            "id": str(uuid4()),
            "report_type": report_type,
            "report_date": str(report_date),
            "ba_name": ba_name.strip(),
            "store_name": store_name.strip(),
            "input_code": normalize_code(code),
            "qty": int(qty),
            "barcode": selected_product["barcode"],
            "product_name": selected_product["product_name"],
            "brand": selected_product["brand"],
            "category": selected_product["category"],
            "notes": notes.strip(),
        }
        save_record(record)
        st.success("Record saved.")


def export_workbook(records: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for report_type, label in REPORT_LABELS.items():
            sheet = records[records["report_type"] == report_type].copy()
            sheet.to_excel(writer, index=False, sheet_name=label)
        records.to_excel(writer, index=False, sheet_name="All Records")
    return output.getvalue()


def admin_page() -> None:
    st.header("Admin Dashboard")
    records = load_records()

    cols = st.columns(5)
    cols[0].metric("Total", len(records))
    for idx, (report_type, label) in enumerate(REPORT_LABELS.items(), start=1):
        cols[idx].metric(label, int((records["report_type"] == report_type).sum()) if not records.empty else 0)

    if records.empty:
        st.info("No BA records yet.")
        return

    st.download_button(
        "Export Excel",
        data=export_workbook(records),
        file_name=f"ba-consignment-export-{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.dataframe(records, hide_index=True, use_container_width=True)


def main() -> None:
    products = load_products()
    st.sidebar.title("Consignment System")
    st.sidebar.caption(f"{len(products):,} products loaded")

    if "user" not in st.session_state:
        login_screen()
        return

    logout_button()
    role = st.session_state.user["role"]
    pages = ["Search", "Admin"] if role == "admin" else ["Record", "Search"]
    page = st.sidebar.radio("Navigation", pages)

    if page == "Record":
        record_page(products)
    elif page == "Search":
        search_page(products)
    elif page == "Admin":
        admin_page()


if __name__ == "__main__":
    main()
