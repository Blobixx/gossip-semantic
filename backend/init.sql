-- Runs as migrator (superuser)

-- Create app user if it does not exist
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles WHERE rolname = 'linkup_user'
   ) THEN
      CREATE USER linkup_user PASSWORD 'password';
   END IF;
END
$$;

-- Create test database if needed
CREATE DATABASE linkup_test;

--------------------------------------------------
-- Enable pgvector
--------------------------------------------------
\c linkup
CREATE EXTENSION IF NOT EXISTS vector;

\c linkup_test
CREATE EXTENSION IF NOT EXISTS vector;

--------------------------------------------------
-- Schema access (REQUIRED)
--------------------------------------------------
\c linkup
GRANT USAGE ON SCHEMA public TO linkup_user;

\c linkup_test
GRANT USAGE ON SCHEMA public TO linkup_user;

--------------------------------------------------
-- Existing tables (important for restore)
--------------------------------------------------
\c linkup
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO linkup_user;

\c linkup_test
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO linkup_user;

--------------------------------------------------
-- Future tables (critical for Alembic)
--------------------------------------------------
\c linkup
ALTER DEFAULT PRIVILEGES FOR ROLE migrator
IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLES
TO linkup_user;

\c linkup_test
ALTER DEFAULT PRIVILEGES FOR ROLE migrator
IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLES
TO linkup_user;
