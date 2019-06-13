CREATE TABLE car_parts_orders
(
    car_parts_id integer,
    orders_name text
);

ALTER TABLE car_parts_orders
ADD CONSTRAINT fk_car_parts_orders_car_parts
FOREIGN KEY (car_parts_id) REFERENCES car_parts(id)
ON DELETE CASCADE DEFERRABLE;

ALTER TABLE car_parts_orders
ADD CONSTRAINT fk_car_parts_orders_orders
FOREIGN KEY (orders_name) REFERENCES orders(name)
ON DELETE CASCADE DEFERRABLE;
