CREATE TABLE IF NOT EXISTS agencies (
    agencie_name VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(agencie_name)
);

CREATE TABLE IF NOT EXISTS trucks (
    truck_name VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(truck_name)
);

CREATE TABLE IF NOT EXISTS clients (
    client_name VARCHAR,
    alternative_name VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    country VARCHAR NOT NULL,
    city VARCHAR,
    agencie VARCHAR,
    truck VARCHAR,
    PRIMARY KEY(client_name),
    FOREIGN KEY(agencie) REFERENCES agencies(agencie_name),
    FOREIGN KEY(truck) REFERENCES trucks(truck_name)
);
