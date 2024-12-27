# Import block according to Python Enhancement Proposal 8 (PEP 8) guidelines.

# Standard library imports
import inspect
import datetime
import os
import sys
import traceback

#from dotenv import load_dotenv
import psycopg2
import pytz
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Third-party imports


# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.logging.system_logging import IotLogging

class DbConnectServer:
    def __init__(self):
        self.__load_config()
        self.connection = None
        self.cursor = None
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_TIMESCALEDB_DB_HOST = os.getenv("SB_TIMESCALEDB_DB_HOST")
        self.SB_TIMESCALEDB_DB_PORT = os.getenv("SB_TIMESCALEDB_DB_PORT")
        self.SB_TIMESCALEDB_DB_NAME = os.getenv("SB_TIMESCALEDB_DB_NAME")
        self.SB_TIMESCALEDB_DB_USER = os.getenv("SB_TIMESCALEDB_DB_USER")
        self.SB_TIMESCALEDB_DB_PASSWORD = os.getenv("SB_TIMESCALEDB_DB_PASSWORD")
        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 

    def connect(self):
        try:
            # Create a connection object
            self.connection = psycopg2.connect(
                host = self.SB_TIMESCALEDB_DB_HOST,
                port = self.SB_TIMESCALEDB_DB_PORT,
                dbname = self.SB_TIMESCALEDB_DB_NAME,
                user = self.SB_TIMESCALEDB_DB_USER,
                password = self.SB_TIMESCALEDB_DB_PASSWORD
            )
            # Create a cursor object
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Connected to database server")
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            self.cursor = None       
            

    # Method for executing SELECT (read-only) queries
    def execute_read(self, query, query_params=None):
        try:
            if not self.cursor: return None # Return None to indicate failure

            self.cursor.execute(query, query_params)
            results = self.cursor.fetchall()  # Fetch the result set
            print(f"SELECT query executed successfully: {query}")
            return results
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            return None  # Return None to indicate failure
    
    def execute_write(self, query, query_params=None):
        # Method for executing data-modifying queries (INSERT, UPDATE, DELETE)
        try:
            if not self.cursor: return False

            self.cursor.execute(query, query_params)
            self.connection.commit()  # Commit changes to the database
            print(f"Modify query executed successfully: {query}")
            return True
        except Exception as e:
            # Log the error and rollback in case of failure
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            self.connection.rollback()  # Rollback in case of error
            return False
    
    def close(self):
        #Close the database connection
        if self.cursor: self.cursor.close()
        if self.connection: self.connection.close()
        print("Database connection closed.")
