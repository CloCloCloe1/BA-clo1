alter table public.products
add column if not exists stc_planogram_location text,
add column if not exists brossard_planogram_location text,
add column if not exists st_laurent_planogram_location text;

update public.products as p
set stc_planogram_location = pl.planogram_location
from public.product_locations as pl
where pl.barcode = p.barcode
  and pl.store_name = 'STC';

update public.products as p
set brossard_planogram_location = pl.planogram_location
from public.product_locations as pl
where pl.barcode = p.barcode
  and pl.store_name = 'Brossard';

update public.products as p
set st_laurent_planogram_location = pl.planogram_location
from public.product_locations as pl
where pl.barcode = p.barcode
  and pl.store_name = 'St.Laurent';

notify pgrst, 'reload schema';
