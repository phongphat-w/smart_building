# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import os
import sqlite3
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Third-party library imports
import pytz  # To handle time zones

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.logging.system_logging import IotLogging # Absolute import

class IotStoreLocalDb:
    def __init__(self, iot_device_id, data):
        self.__load_config()
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)
        self.iot_device_id = iot_device_id
        self.data = data
    
    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 

    def store_data(self):
        """
        Store data in IOT local DB (SQLite)
        """
        conn = None
        try:
            db_filename = os.path.join(self.root_path, "database", "iot_local_db" , f"{self.iot_device_id}.sqlite3")
            
            if not os.path.exists(db_filename):
                print(f"Database {db_filename} does not exist. Creating a new database.")
                conn = sqlite3.connect(db_filename)
                cursor = conn.cursor()
                
                # Create the table if the database is new
                cursor.execute(f"""
                                CREATE TABLE IF NOT EXISTS iot_data (
                                    data_id TEXT PRIMARY KEY,
                                    device_id TEXT,
                                    measured_at TEXT,
                                    sensor_type TEXT,
                                    sensor_value REAL,
                                    created_at TEXT,
                                    auto_mode INTERGER,
                                    synced_flag INTEGER                         
                                ); """
                            )
                conn.commit()  # Commit the transaction to create the table
            else:
                # If database exists, just connect to it
                conn = sqlite3.connect(db_filename)
                cursor = conn.cursor()
                query = """
                            INSERT INTO iot_data (
                                data_id,
                                device_id,
                                measured_at,
                                sensor_type,
                                sensor_value,
                                created_at,
                                auto_mode,
                                synced_flag
                            ) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
                data_tuple = [
                                (
                                    row["data_id"],
                                    row["device_id"],
                                    row["measured_at"],
                                    row["sensor_type"],
                                    row["sensor_value"],
                                    row["created_at"],
                                    row["auto_mode"],
                                    row["synced_flag"]
                                ) for row in self.data
                            ]
                cursor.executemany(query, data_tuple)
                conn.commit()
            #
            return True
        except Exception as e:
            conn.rollback()
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.log.logger.error(error_msg)
            return False
        
        finally:
            if conn: conn.close()
        
          
