create table if not exists public.ba_users (
  username text primary key,
  password_hash text not null,
  salt text not null,
  display_name text not null,
  store_name text,
  location text,
  active boolean default true,
  created_at timestamptz default now()
);

alter table public.ba_users enable row level security;

drop policy if exists "Allow app read ba users" on public.ba_users;
drop policy if exists "Allow app insert ba users" on public.ba_users;

create policy "Allow app read ba users"
on public.ba_users
for select
to anon, authenticated
using (true);

create policy "Allow app insert ba users"
on public.ba_users
for insert
to anon, authenticated
with check (true);

grant select, insert on table public.ba_users to anon, authenticated;

notify pgrst, 'reload schema';
