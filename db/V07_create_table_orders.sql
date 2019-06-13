CREATE TABLE orders
(
    id serial PRIMARY KEY,
    begin_date timestamp DEFAULT now(),
    end_date timestamp DEFAULT NULL,
    company text,
    number integer CHECK(number > 0),
    total_price price_type,
    car_parts_id integer
);

ALTER TABLE orders
ADD CONSTRAINT fk_orders_car_parts
FOREIGN KEY (car_parts_id) REFERENCES car_parts(id)
ON DELETE SET NULL DEFERRABLE;
