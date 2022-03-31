CREATE TABLE public.trips (
	region varchar NULL,
	origin_coord_lat float8 NULL,
	origin_coord_long float8 NULL,
	destination_coord_lat float8 NULL,
	destination_coord_long float8 NULL,
	datetime timestamp NULL,
	datasource varchar NULL
);