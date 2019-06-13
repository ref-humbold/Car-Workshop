CREATE TABLE cars
(
    model text PRIMARY KEY,
    mark text NOT NULL,
    type auto_type,
    weight double precision CHECK(weight > 0)
);
