CREATE TABLE car_parts_cars
(
    car_parts_id integer,
    cars_model text
);

ALTER TABLE car_parts_cars
ADD CONSTRAINT fk_car_parts_cars_car_parts
FOREIGN KEY (car_parts_id) REFERENCES car_parts(id)
ON DELETE CASCADE DEFERRABLE;

ALTER TABLE car_parts_cars
ADD CONSTRAINT fk_car_parts_cars_cars
FOREIGN KEY (cars_model) REFERENCES cars(model)
ON DELETE CASCADE DEFERRABLE;
