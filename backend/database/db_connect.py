import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from dotenv import load_dotenv
import inspect

class DbConnect:
    def __init__(self, root_path):
        self.connection = None
        self.cursor = None
        load_dotenv(dotenv_path = os.path.join(root_path, "configuration", ".env"))

    def connect(self):
        try:
            # Create a connection object
            self.connection = psycopg2.connect(
                host = os.getenv("SB__TIMESCALEDB_DB_HOST"),
                port = os.getenv("SB__TIMESCALEDB_DB_PORT"),
                dbname = os.getenv("SB__TIMESCALEDB_DB_NAME"),
                user = os.getenv("SB__TIMESCALEDB_DB_USER"),
                password = os.getenv("SB__TIMESCALEDB_DB_PASSWORD") 
            )

            # Create a cursor object
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Connected to the PostgreSQL database")

        except Exception as e:
            print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
            raise Exception("Unable to connect to the database.")

    #Execute a query and return results.
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"Query executed successfully: {query}")
            return json.loads(json.dumps(self.cursor.fetchall()))
        except Exception as e:
            print(f"""{inspect.currentframe().f_code.co_name}(): Query - {query}""")
            print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
            self.connection.rollback()
            return json.dumps([])

    #Close the database connection
    def close(self):
        
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
