# Admin User SOP

## Purpose

The Admin page is used to review BA submissions, filter records by location, and export Excel files for company reporting.

## App Link

[APP LINK]

## Admin Login

1. Open the app link.
2. Go to `Sign in`.
3. Enter the admin username and password.
4. Click `Sign in`.

Current admin username:

```text
admin
```

The admin password is managed in Streamlit Secrets.

## Navigation

After login, Admin users will see:

- `Search`: search the product master list.
- `Admin`: review records and export Excel files.

Admin users do not need the BA record entry page.

## Review Records

1. Go to `Admin`.
2. Review the dashboard metrics:
   - Total
   - Tester
   - Damage
   - Theft
   - Restock
3. Use the `Location` dropdown to filter records.

Location examples:

- `BRO`
- `STL`
- Other store-specific locations

## Export Excel

To export records:

1. Go to `Admin`.
2. Select a location from the `Location` dropdown, or choose `All locations`.
3. Click `Export selected location Excel`.

The exported Excel file contains separate sheets:

- Tester
- Damage
- Theft
- Restock
- All Records

## Download Each Location Separately

If multiple locations exist:

1. Go to `Admin`.
2. Open `Download each location separately`.
3. Click the download button for the location you need.

This is useful when separate files are needed for different stores or locations.

## Excel Column Order

The export uses this column order:

1. Date
2. BA Name
3. Last6
4. Full Barcode
5. Product Name
6. Brand
7. Qty
8. Category
9. Store Name
10. Location
11. Report Type
12. Notes

## Manage BA Accounts

BA accounts created through registration are stored in Supabase table:

```text
ba_users
```

To view BA accounts:

1. Open Supabase.
2. Go to `Table Editor`.
3. Open `ba_users`.

To deactivate a BA account:

```sql
update public.ba_users
set active = false
where username = 'ba_username';
```

To delete a test BA account:

```sql
delete from public.ba_users
where username = 'ba_username';
```

## Manage Registration Code

The BA registration code is managed in Streamlit Secrets:

```toml
REGISTRATION_CODE = "YOUR-CODE"
```

After changing the registration code:

1. Save Streamlit Secrets.
2. Reboot or redeploy the app.
3. Share the new code only with authorized BA users.

## Common Admin Checks

- Confirm BA records are saved in the `records` table.
- Confirm Store and Location values are entered correctly.
- Export and review the Excel file before sending it internally.
- If a BA reports a wrong product from a previous day, Admin should correct the record directly in Supabase or ask the BA to submit a corrected record.
