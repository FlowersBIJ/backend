CREATE TABLE IF NOT EXISTS order_types (
    typename VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(typename)
);

CREATE TABLE IF NOT EXISTS orders (
    id uuid DEFAULT uuid_generate_v4(),
    manager_name VARCHAR NOT NULL,
    comment VARCHAR,
    outcome_invoice VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    order_type VARCHAR NOT NULL,
    client_name VARCHAR NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(order_type) REFERENCES order_types(typename),
    FOREIGN KEY(client_name) REFERENCES clients(client_name),
    UNIQUE(client_name, outcome_invoice)
);