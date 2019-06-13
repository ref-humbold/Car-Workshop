CREATE OR REPLACE FUNCTION orders_trigger_func()
RETURNS TRIGGER AS
$f$
BEGIN
    IF OLD.end_date IS NULL AND NEW.end_date IS NOT NULL
    THEN
        UPDATE car_parts SET number = number + NEW.number WHERE id = NEW.car_parts_id;
    ELSIF OLD.number <> NEW.number
    THEN
        UPDATE car_parts SET number = number - OLD.number + NEW.number WHERE id = NEW.car_parts_id;
    END IF;

    RETURN NULL;
END;
$f$
LANGUAGE plpgsql;

CREATE TRIGGER orders_trigger
AFTER UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE orders_trigger_func();
