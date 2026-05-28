alter table public.records
add column if not exists submitted_by text;

update public.records
set submitted_by = lower(regexp_replace(coalesce(ba_name, ''), '\s+', '', 'g'))
where coalesce(submitted_by, '') = '';

notify pgrst, 'reload schema';
