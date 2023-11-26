CREATE TABLE IF NOT EXISTS flowers (
    flower_name VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(flower_name)
);

CREATE TABLE IF NOT EXISTS flower_sorts (
    flower_name VARCHAR,
    flower_sort VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(flower_name, flower_sort),
    FOREIGN KEY(flower_name) REFERENCES flowers(flower_name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS flowers_length (
    flower_name VARCHAR,
    flower_sort VARCHAR,
    flower_length VARCHAR,
    visible BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(flower_name, flower_sort, flower_length),
    FOREIGN KEY(flower_name, flower_sort) REFERENCES flower_sorts(flower_name, flower_sort) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS flowers_in_box (
    id uuid DEFAULT uuid_generate_v4(),
    stems INTEGER NOT NULL,
    income_price NUMERIC(1000, 2) NOT NULL CHECK (income_price>0),
    outcome_price NUMERIC(1000, 2) CHECK (outcome_price>0),
    hotline_miami_price NUMERIC(1000, 2) CHECK (hotline_miami_price>0),
    visible BOOLEAN NOT NULL DEFAULT true,
    box_id uuid,
    flower_name VARCHAR,
    flower_sort VARCHAR,
    flower_length VARCHAR,
    PRIMARY KEY(id),
    FOREIGN KEY(box_id) REFERENCES boxes(id) ON DELETE CASCADE,
    FOREIGN KEY(flower_name, flower_sort, flower_length) REFERENCES flowers_length(flower_name, flower_sort, flower_length)
);