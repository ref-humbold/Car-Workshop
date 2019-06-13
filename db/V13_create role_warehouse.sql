CREATE ROLE warehouse;

GRANT SELECT ON car_parts TO warehouse;

GRANT SELECT, INSERT, UPDATE ON orders TO warehouse;
