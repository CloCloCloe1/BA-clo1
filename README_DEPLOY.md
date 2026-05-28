# Miniso BA Consignment MVP

This is the free/fast test version:

- GitHub: stores this code
- Streamlit Community Cloud: hosts the URL
- Supabase Free: optional backend database for shared products and records

## Demo Accounts

- BA: `ba / ba123`
- Admin: `admin / Nakama-clo1`

For production, change these passwords in Streamlit Secrets.

## Local Test

```powershell
cd C:\Users\limin\Documents\Codex\2026-05-28\process-conignment-stores-ediable-excel-ba\miniso-streamlit-mvp
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run streamlit_app.py
```

If `streamlit` is not available from your terminal, use your Python environment:

```powershell
python -m streamlit run streamlit_app.py
```

## Supabase Setup

1. Create a free Supabase project.
2. Open `SQL Editor`.
3. Paste and run `supabase_schema.sql`.
4. Copy your Project URL and API key.

## Import Miniso Product Master To Supabase

Set environment variables:

```powershell
$env:SUPABASE_URL="https://your-project.supabase.co"
$env:SUPABASE_KEY="your-service-role-or-api-key"
python import_products.py
```

This imports `data/products.csv`, which was extracted from the Miniso `Product Master` sheet.

## Streamlit Cloud Deploy

1. Create a GitHub repository, for example `miniso-ba-consignment-mvp`.
2. Upload everything inside this folder.
3. Go to <https://share.streamlit.io>.
4. Click `Create app`.
5. Select your GitHub repo.
6. Main file path: `streamlit_app.py`.
7. Open `Advanced settings`.
8. Paste secrets:

```toml
USE_SUPABASE = true
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-api-key"
REGISTRATION_CODE = "change-this-ba-registration-code"

[users.admin]
password = "Nakama-clo1"
role = "admin"
display_name = "Admin User"

[users.ba]
password = "change-this-ba-password"
role = "ba"
display_name = "BA User"
store_name = "Miniso"
location = "BRO"
```

9. Click `Deploy`.
10. Streamlit gives you a URL like:

```text
https://your-app-name.streamlit.app
```

## First MVP Scope

- Miniso products only
- BA enters tester/damage/theft/restock records
- BA can review and edit their own records from today
- Search by barcode, last 6, product name, or brand
- Admin sees all records
- Admin can filter/download records by location
- BA can register accounts with the registration code
- Admin exports one Excel file with four sheets:
  - Tester
  - Damage
  - Theft
  - Restock

## Later Upgrade

- Admin upload new master list
- Multiple customers: Miniso, TNT, others
- Multiple stores per customer
- Import batches and active/inactive master lists
- One account per BA
