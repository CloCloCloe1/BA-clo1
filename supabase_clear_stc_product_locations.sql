delete from public.product_locations
where store_name = 'STC';

notify pgrst, 'reload schema';
