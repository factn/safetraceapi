--SCRIPT USED TO INITIALIZE THE DB

-- TODO: check if i need a readonly trigger for serial id's...

DROP TABLE IF EXISTS clients, devices, ep_permissions, events CASCADE;

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    display_name VARCHAR(512) NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,            -- hashed
    bio VARCHAR(4096) NOT NULL,
    api_key VARCHAR(128) UNIQUE NOT NULL,     -- encrypted      
    public_key VARCHAR(66) UNIQUE NOT NULL,
    private_key VARCHAR(192) UNIQUE NOT NULL  -- encrypted
);

-- INSERT SAFETRACE ACCOUNT (TEMPORARY), need public key in order to give permissions
INSERT INTO clients (email, display_name, password, bio, api_key, public_key, private_key) VALUES ('#', 'SafetraceAPI', '#', 'SafetraceAPI BIO', '#', '03edad0f6cfeeee940ac302278042eb0d07113e2c83256b8703a25714540f667a0', '#');

CREATE TABLE devices (
    device_id VARCHAR(64) UNIQUE NOT NULL PRIMARY KEY,  -- hashed
    device_key VARCHAR(64) UNIQUE NOT NULL              -- hashed
);
CREATE TABLE ep_permissions (
    device_id VARCHAR(64) NOT NULL,           -- hashed
    
    -- the Client / EP to which the device owner has given permission to access their data
    client_id INTEGER NOT NULL,
    
    -- the resource owner's key to decrypt their data, encrypted with the client's public key
    device_key VARCHAR(322) UNIQUE NOT NULL,  -- encrypted
    
    PRIMARY KEY(device_id, client_id),
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL DEFAULT NOW(),

    device_id VARCHAR(64) NOT NULL,               -- from devices table
    
    row_type INTEGER NOT NULL CONSTRAINT row_type_range_error CHECK (row_type >= 0 AND row_type <= 2),              
    -- [0: GPS] -- [1: BlueTooth] -- [2: Survey]
    
    -- GPS
    longitude VARCHAR(512), -- encrypted
    CONSTRAINT longitude_null_error CHECK (row_type != 0 OR (longitude IS NOT NULL)),
    CONSTRAINT longitude_not_null_error CHECK (row_type = 0 OR (longitude IS NULL)),
    latitude VARCHAR(512), -- encrypted
    CONSTRAINT latitude_null_error CHECK (row_type != 0 OR (latitude IS NOT NULL)),
    CONSTRAINT latitude_not_null_error CHECK (row_type = 0 OR (latitude IS NULL)),

    -- Blue Tooth
    contact_id VARCHAR(64) CONSTRAINT contact_id_is_device_id_error CHECK (contact_id != device_id), -- from devices table (hashed)
    CONSTRAINT contact_id_null_error CHECK (row_type != 1 OR (contact_id IS NOT NULL)),
    CONSTRAINT contact_id_not_null_error CHECK (row_type = 1 OR (contact_id IS NULL)),
    contact_level VARCHAR(512), -- encrypted
    CONSTRAINT contact_level_null_error CHECK (row_type != 1 OR (contact_level IS NOT NULL)),
    CONSTRAINT contact_level_not_null_error CHECK (row_type = 1 OR (contact_level IS NULL)),

    -- Survey
    symptoms VARCHAR(4098), -- encrypted
    CONSTRAINT symptoms_null_error CHECK (row_type != 2 OR (symptoms IS NOT NULL)),
    CONSTRAINT symptoms_not_null_error CHECK (row_type = 2 OR (symptoms IS NULL)),
    infection_status VARCHAR(512), -- encrypted
    CONSTRAINT infection_status_null_error CHECK (row_type != 2 OR (infection_status IS NOT NULL)),
    CONSTRAINT infection_status_not_null_error CHECK (row_type = 2 OR (infection_status IS NULL)),

    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES devices(device_id) ON DELETE CASCADE
);
