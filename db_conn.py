# to connect to a database and wait for it to ce ready

import logging
import time


def wait_for_db_connection(db_path:str, timeout: int = 5) -> None:
    """Wait for the Django database to be ready"""
    from django.db import connections
    from django.db.utils import OperationalError

    retries = timeout
    for i in range(retries):
        try:
            connections["default"].cursor()
            logging.info("Database is ready")
        except OperationalError:
            logging.warning(f"Database not ready yet. Retrying {i+1}/{retries}...")
            time.sleep(timeout) # Wait before retrying
    raise RuntimeError("Database could not be reached after multiple retries")

# Export the function to be use to connecto mqtt client to a database

wait_for_db_connection()

