CREATE TABLE clients
(
    id serial PRIMARY KEY,
    first_name text,
    last_name text,
    phone phone_type,
    company text DEFAULT NULL,
    discount percent_type
);
