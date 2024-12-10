# Import block according to Python Enhancement Proposal 8 (PEP 8) guidelines.

# Standard library imports
import inspect
import json
import logging
import os
#from dotenv import load_dotenv

# Third-party imports
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Local application/library imports
# N/A

db_logger = logging.getLogger('django.db.backends')
logger = logging.getLogger(__name__)

class DbConnect:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            # Create a connection object
            self.connection = psycopg2.connect(
                host = os.getenv("SB_TIMESCALEDB_DB_HOST"),
                port = os.getenv("SB_TIMESCALEDB_DB_PORT"),
                dbname = os.getenv("SB_TIMESCALEDB_DB_NAME"),
                user = os.getenv("SB_TIMESCALEDB_DB_USER"),
                password = os.getenv("SB_TIMESCALEDB_DB_PASSWORD") 
            )

            # Create a cursor object
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Connected to the PostgreSQL database")

        except Exception as e:
            print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
            logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
            raise Exception("Unable to connect to the database.")

    #Execute a query and return results.
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()

            for query in self.connection.queries:
                db_logger.debug(f"SQL Query: {query['sql']} | Time Taken: {query['time']} ms")

            print(f"Query executed successfully: {query}")
            return json.loads(json.dumps(self.cursor.fetchall()))
        
        except Exception as e:
            print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
            print(f"""{inspect.currentframe().f_code.co_name}(): Query - {query}""")
            logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
            self.connection.rollback()
            return json.dumps([])

    #Close the database connection
    def close(self):
        
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
