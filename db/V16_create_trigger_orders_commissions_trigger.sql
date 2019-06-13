CREATE OR REPLACE FUNCTION orders_commissions_trigger_func()
RETURNS TRIGGER AS
$f$
BEGIN
    WITH tab AS
    (
        SELECT orders.id, sum(commissions.cena)
        FROM orders
             JOIN orders_commissions ON orders_commissions.orders_id = orders.id
             JOIN commissions ON orders_commissions.commissions_name = commissions.name
        GROUP BY orders.id
        HAVING orders.id = NEW.orders_id
    )
    UPDATE orders SET total_price = tab.sum
    FROM tab
    WHERE orders.id = tab.id;

    RETURN NULL;
END;
$f$
LANGUAGE plpgsql;

CREATE TRIGGER orders_commissions_trigger
AFTER INSERT OR UPDATE ON orders_commissions
FOR EACH ROW EXECUTE PROCEDURE orders_commissions_trigger_func();
