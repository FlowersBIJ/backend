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

CREATE TABLE IF NOT EXISTS income_invoices (
    id uuid DEFAULT uuid_generate_v4(),
    invoice VARCHAR NOT NULL,
    plantation VARCHAR NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(plantation) REFERENCES plantations(plantation_name)
);

CREATE TABLE IF NOT EXISTS boxes (
    id uuid DEFAULT uuid_generate_v4(),
    release_date DATE,
    box_count INTEGER CHECK(box_count > 0),
    visible BOOLEAN NOT NULL DEFAULT true,
    box_type VARCHAR NOT NULL,
    order_id uuid NOT NULL,
    invoice_id uuid,
    PRIMARY KEY(id),
    FOREIGN KEY(box_type) REFERENCES box_types(typename),
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY(invoice_id) REFERENCES income_invoices(id)
);