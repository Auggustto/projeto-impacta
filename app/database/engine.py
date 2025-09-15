import os
import psycopg2
from psycopg2 import OperationalError

from app.utils.logger import logger

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

CREATE_TABLE_PRODUCT_SQL = """
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TRIGGER_UPDATED_AT_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_trigger
        WHERE tgname = 'update_product_updated_at'
    ) THEN
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER update_product_updated_at
        BEFORE UPDATE ON product
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
    END IF;
END
$$;
"""

def get_connection():
    try:
        conn = psycopg2.connect(conn_str)
        logger.info("Connection successfully established!")
        return conn
    except OperationalError as e:
        logger.error(f"Connection error! {e}")
        return None


def init_db():
    conn = get_connection()
    if not conn:
        logger.error("Database connection failed during init_db.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_PRODUCT_SQL)
            cur.execute(CREATE_TRIGGER_UPDATED_AT_SQL)
        conn.commit()
        logger.info("Tables and triggers initialized successfully.")
    except Exception as e:
        logger.error(f"Error during DB initialization: {e}")
    finally:
        conn.close()
