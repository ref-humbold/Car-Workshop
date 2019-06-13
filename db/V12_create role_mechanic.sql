CREATE ROLE mechanic;

GRANT SELECT ON cars, commissions, orders TO mechanic;

GRANT SELECT, INSERT, UPDATE ON car_parts, car_parts_cars, car_parts_orders TO mechanic;

GRANT UPDATE(end_date) ON commissions TO mechanic;
