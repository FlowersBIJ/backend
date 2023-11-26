CREATE TABLE IF NOT EXISTS box_types (
    typename VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(typename)
);

CREATE TABLE IF NOT EXISTS plantations (
    plantation_name VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(plantation_name)
);

CREATE TABLE IF NOT EXISTS boxes (
    id uuid DEFAULT uuid_generate_v4(),
    income_invoice VARCHAR,
    box_number INTEGER,
    visible BOOLEAN NOT NULL DEFAULT true,
    box_type VARCHAR,
    plantation VARCHAR,
    order_id uuid,
    PRIMARY KEY(id),
    FOREIGN KEY(box_type) REFERENCES box_types(typename),
    FOREIGN KEY(plantation) REFERENCES plantations(plantation_name),
    FOREIGN KEY(order_id) REFERENCES orders(id)
);