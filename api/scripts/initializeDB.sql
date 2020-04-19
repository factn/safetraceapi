--SCRIPT USED TO INITIALIZE THE DB


DO $$ DECLARE
  r RECORD;
BEGIN
  FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
    EXECUTE 'DROP TABLE ' || quote_ident(r.tablename) || ' CASCADE';
  END LOOP;
END $$;

-- CREATE TABLE areas (
--     area_id INTEGER NOT NULL PRIMARY KEY,
--     longitude NUMERIC NOT NULL CONSTRAINT longitude_range_error CHECK (longitude >= -180 AND longitude <= 180),
--     latitude NUMERIC NOT NULL CONSTRAINT latitude_range_error CHECK (latitude >= -90 AND latitude <= 90),
--     radius INTEGER NOT NULL CONSTRAINT radius_range_error CHECK (radius >= 0)
-- );

CREATE TABLE nodes (
    node_id INTEGER NOT NULL PRIMARY KEY,
    public_key VARCHAR(66) NOT NULL
);

INSERT INTO nodes (node_id, public_key) VALUES 
(1, '03e49a88bf6889414e27890ed1f29c615cdfe22aff448b7396ced9c05a29a150d0'),
(2, '0389c6a273d34941bddd01af256f5a460870fe74064e45dc2ad74c9a15df040090'),
(3, '02c1cdca9a7491b807fe64a2bcf719086e46f0ecc9ff510a3771b94d9a788e2bd7');


CREATE TABLE triples (
    triple_id VARCHAR(128) NOT NULL,
    node_id INTEGER NOT NULL,
    share TEXT NOT NULL,

    PRIMARY KEY(triple_id, node_id),
    FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE
);

CREATE TABLE shares (
    device_id VARCHAR(36) NOT NULL,
    computation_id VARCHAR(20) NOT NULL,
    node_id INTEGER NOT NULL,
    share VARCHAR(4096) NOT NULL,

    PRIMARY KEY(device_id, computation_id, node_id),    
    FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE
);

CREATE TABLE results (
    node_id INTEGER NOT NULL,
    computation_id VARCHAR(20) NOT NULL,
    area_id INTEGER NOT NULL,
    share VARCHAR(8192) NOT NULL,
    
    PRIMARY KEY(area_id, computation_id, node_id),    
    FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE--,
    -- FOREIGN KEY (area_id) REFERENCES areas(area_id) ON DELETE CASCADE
);
