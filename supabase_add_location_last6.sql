alter table public.records
add column if not exists last6 text;

alter table public.records
add column if not exists location text;

update public.records
set last6 = right(coalesce(input_code, barcode, ''), 6)
where coalesce(last6, '') = '';

create index if not exists idx_records_location on public.records(location);

notify pgrst, 'reload schema';
