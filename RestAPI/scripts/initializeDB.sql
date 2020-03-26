--SCRIPT USED TO INITIALIZE THE DB

-- TODO: check if i need a readonly trigger for serial id's...

DROP TABLE IF EXISTS main_table, users, events CASCADE;

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY, -- user / device id
  phone_number BIGINT UNIQUE NOT NULL
);

CREATE TABLE events (
  event_id SERIAL PRIMARY KEY,
  time TIMESTAMP NOT NULL DEFAULT NOW(),
  user_id INTEGER NOT NULL,               -- from users table
  
  row_type INTEGER NOT NULL CONSTRAINT row_type_range_error CHECK (row_type >= 0 AND row_type <= 2),              
  -- [0: GPS] -- [1: BlueTooth] -- [2: Survey]
  
  -- GPS
  longitude NUMERIC CONSTRAINT longitude_range_error CHECK (longitude >= -180 AND longitude <= 180),
  CONSTRAINT longitude_null_error CHECK (row_type != 0 OR (longitude IS NOT NULL)),
  CONSTRAINT longitude_not_null_error CHECK (row_type = 0 OR (longitude IS NULL)),
  latitude NUMERIC CONSTRAINT latitude_range_error CHECK (latitude >= -90 AND latitude <= 90),
  CONSTRAINT latitude_null_error CHECK (row_type != 0 OR (latitude IS NOT NULL)),
  CONSTRAINT latitude_not_null_error CHECK (row_type = 0 OR (latitude IS NULL)),

  -- Blue Tooth
  contact_id INTEGER CONSTRAINT contact_id_is_user_id_error CHECK (contact_id != user_id), -- from users table
  CONSTRAINT contact_id_null_error CHECK (row_type != 1 OR (contact_id IS NOT NULL)),
  CONSTRAINT contact_id_not_null_error CHECK (row_type = 1 OR (contact_id IS NULL)),
  contact_level NUMERIC,
  CONSTRAINT contact_level_null_error CHECK (row_type != 1 OR (contact_level IS NOT NULL)),
  CONSTRAINT contact_level_not_null_error CHECK (row_type = 1 OR (contact_level IS NULL)),

  -- Survey
  symptoms VARCHAR(4098),                 -- comma seperated string...
  CONSTRAINT symptoms_null_error CHECK (row_type != 2 OR (symptoms IS NOT NULL)),
  CONSTRAINT symptoms_not_null_error CHECK (row_type = 2 OR (symptoms IS NULL)),
  infection_status INTEGER CONSTRAINT infection_status_range_error CHECK (infection_status >= 0 AND infection_status <= 3),
  -- [0 opt out (dont want to say)] -- [1 dont know] -- [2 infected] -- [3 recovered]
  CONSTRAINT infection_status_null_error CHECK (row_type != 2 OR (infection_status IS NOT NULL)),
  CONSTRAINT infection_status_not_null_error CHECK (row_type = 2 OR (infection_status IS NULL)),

  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (contact_id) REFERENCES users(user_id) ON DELETE CASCADE
);
