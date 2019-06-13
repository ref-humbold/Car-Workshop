CREATE TABLE car_parts
(
    id serial PRIMARY KEY,
    producer text,
    number integer CHECK(number >= 0),
    type text,
    universal boolean DEFAULT TRUE
);
