--CREATE TABLE main_table (
--  event_id SERIAL PRIMARY KEY,
--  user_id VARCHAR(512) NOT NULL,
--  encryption VARCHAR(64) NOT NULL,
--  time VARCHAR(512) NOT NULL,
--  location_type VARCHAR(128) NOT NULL,
--  location VARCHAR(512) NOT NULL,
--  symptoms VARCHAR(4098) NOT NULL
--);

INSERT INTO main_table (user_id, encryption, time, location_type, location, symptoms) VALUES ('0', 'mpc', '12:12:12', 'gps', 'lat:24.444|lon:75.05', 'headache, cough, sore throat');