CREATE ROLE seller;

GRANT SELECT ON cars, orders TO seller;

GRANT SELECT, INSERT, UPDATE ON clients, commissions, orders_commissions TO seller;
