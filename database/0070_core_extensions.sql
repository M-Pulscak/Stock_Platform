ALTER TABLE core.assets
ADD COLUMN sector        TEXT,
ADD COLUMN industry      TEXT,
ADD COLUMN country       TEXT,
ADD COLUMN website       TEXT,
ADD COLUMN employees     INTEGER;