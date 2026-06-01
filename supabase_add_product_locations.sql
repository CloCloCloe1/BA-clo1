create table if not exists public.product_locations (
  barcode text not null,
  store_name text not null,
  planogram_location text not null,
  brand text,
  product_name text,
  updated_at timestamptz default now(),
  primary key (barcode, store_name)
);

create index if not exists idx_product_locations_store
on public.product_locations(store_name);

create index if not exists idx_product_locations_barcode
on public.product_locations(barcode);

alter table public.product_locations enable row level security;

drop policy if exists "Allow anon read product locations" on public.product_locations;
drop policy if exists "Allow anon insert product locations" on public.product_locations;
drop policy if exists "Allow anon update product locations" on public.product_locations;
drop policy if exists "Allow anon delete product locations" on public.product_locations;

create policy "Allow anon read product locations"
on public.product_locations
for select
to anon, authenticated
using (true);

create policy "Allow anon insert product locations"
on public.product_locations
for insert
to anon, authenticated
with check (true);

create policy "Allow anon update product locations"
on public.product_locations
for update
to anon, authenticated
using (true)
with check (true);

create policy "Allow anon delete product locations"
on public.product_locations
for delete
to anon, authenticated
using (true);

notify pgrst, 'reload schema';
