create table if not exists products (
  barcode text primary key,
  last6 text,
  product_name text,
  brand text,
  status text,
  msl text,
  max_qty text,
  updated_at timestamptz default now()
);

create table if not exists records (
  id uuid primary key default gen_random_uuid(),
  report_type text not null check (report_type in ('tester', 'damage', 'theft', 'restock')),
  report_date date not null,
  ba_name text not null,
  store_name text,
  input_code text,
  last6 text,
  location text,
  submitted_by text,
  qty integer not null,
  barcode text,
  product_name text,
  brand text,
  notes text,
  created_at timestamptz default now()
);

create table if not exists ba_users (
  username text primary key,
  password_hash text not null,
  salt text not null,
  display_name text not null,
  store_name text,
  location text,
  active boolean default true,
  created_at timestamptz default now()
);

create index if not exists idx_products_last6 on products(last6);
create index if not exists idx_records_report_type on records(report_type);
create index if not exists idx_records_location on records(location);
create index if not exists idx_records_created_at on records(created_at);
