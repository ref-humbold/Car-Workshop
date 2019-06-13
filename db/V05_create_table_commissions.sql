CREATE TABLE commissions
(
    id serial PRIMARY KEY,
    begin_date timestamp DEFAULT now(),
    end_date timestamp DEFAULT NULL,
    registration registration_type,
    invoice boolean DEFAULT FALSE,
    price price_type,
    clients_id integer,
    cars_model text
);

ALTER TABLE commissions
ADD CONSTRAINT fk_commissions_clients
FOREIGN KEY (clients_id) REFERENCES clients(id)
ON DELETE SET NULL DEFERRABLE;

ALTER TABLE commissions
ADD CONSTRAINT fk_commissions_cars
FOREIGN KEY (cars_model) REFERENCES cars(model)
ON DELETE SET NULL DEFERRABLE;
