CREATE TABLE orders_commissions
(
    orders_id integer,
    commissions_name text
);

ALTER TABLE orders_commissions
ADD CONSTRAINT fk_orders_commissions_orders
FOREIGN KEY (orders_id) REFERENCES orders(id)
ON DELETE CASCADE DEFERRABLE;

ALTER TABLE orders_commissions
ADD CONSTRAINT fk_orders_commissions_commissions
FOREIGN KEY (commissions_name) REFERENCES commissions(name)
ON DELETE SET NULL DEFERRABLE;
