CREATE TABLE password_change_status
(
username name PRIMARY KEY,
security_status boolean
);

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';

CREATE GROUP new_project_admins WITH USER postgres;
