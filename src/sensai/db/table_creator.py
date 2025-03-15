# db/table_creator.py
import logging
from typing import Optional
from .supabase_client import get_db_connection
from .schemas import TABLE_SCHEMAS

from util import logger_setup

# Initialize logger
logger = logging.getLogger(__name__)

def create_table(table_name: str, schema: Optional[str] = None) -> bool:
    """Create a table in Supabase."""
    try:
        if schema is None:
            if table_name not in TABLE_SCHEMAS:
                logger.error(f"No schema defined for '{table_name}'.")
                return False
            schema = TABLE_SCHEMAS[table_name]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(schema)
        conn.commit()
        logger.info(f"Table '{table_name}' created or already exists.")
        return True
    except Exception as e:
        logger.error(f"Error creating table '{table_name}': {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def create_all_tables() -> None:
    """Create all tables defined in TABLE_SCHEMAS."""
    for table_name in TABLE_SCHEMAS.keys():
        create_table(table_name)



if __name__ == "__main__":
    # Fetch schema from schemas.py
    create_table(table_name="temperature_readings")

    # Provide schema for a users table
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """

    success = create_table(table_name="users", schema=schema)

    if success:
        logger.info("Table created successfully!")
    else:
        logger.error("Failed to create table!")