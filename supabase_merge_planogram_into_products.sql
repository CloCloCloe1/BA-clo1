alter table public.products
add column if not exists stc_planogram_location text,
add column if not exists brossard_planogram_location text,
add column if not exists st_laurent_planogram_location text;

update public.products as p
set stc_planogram_location = matched.planogram_location
from (
  select distinct on (right(barcode, 6))
    barcode,
    right(barcode, 6) as last6,
    planogram_location
  from public.product_locations
  where store_name = 'STC'
  order by right(barcode, 6), barcode
) as matched
where matched.barcode = p.barcode
   or matched.last6 = p.last6;

update public.products as p
set brossard_planogram_location = matched.planogram_location
from (
  select distinct on (right(barcode, 6))
    barcode,
    right(barcode, 6) as last6,
    planogram_location
  from public.product_locations
  where store_name = 'Brossard'
  order by right(barcode, 6), barcode
) as matched
where matched.barcode = p.barcode
   or matched.last6 = p.last6;

update public.products as p
set st_laurent_planogram_location = matched.planogram_location
from (
  select distinct on (right(barcode, 6))
    barcode,
    right(barcode, 6) as last6,
    planogram_location
  from public.product_locations
  where store_name = 'St.Laurent'
  order by right(barcode, 6), barcode
) as matched
where matched.barcode = p.barcode
   or matched.last6 = p.last6;

notify pgrst, 'reload schema';
