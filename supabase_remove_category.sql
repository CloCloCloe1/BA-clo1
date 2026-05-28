alter table public.records
drop column if exists category;

alter table public.products
drop column if exists category;

notify pgrst, 'reload schema';
