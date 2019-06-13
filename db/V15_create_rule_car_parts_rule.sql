CREATE OR REPLACE RULE car_parts_rule AS
    ON INSERT TO car_parts_cars
    DO ALSO UPDATE car_parts
            SET universal = FALSE
            WHERE car_parts.id = NEW.car_parts_id;
