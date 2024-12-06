import json
from datetime import datetime 
import time
import pytz  # To handle time zones
import sqlite3
import random
import uuid
import os
from dotenv import load_dotenv
import inspect

con_iot_device_id = "96b38698-d9ad-4355-807f-5580397471a1" #Presence sensors
root_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

# Load environment variables from .env file
load_dotenv(dotenv_path = os.path.join(root_path, "", ".env"))
            
def gen_data(iot_device_id, auto_mode = 1, file_name=""):
    lis_data = []
    try:
        if auto_mode == 1:
            # Define data for each device type    
            if iot_device_id == con_iot_device_id:
                
                object_status = {
                    "data_id": str(uuid.uuid4()),
                    "device_id": iot_device_id,
                    "measured_at": str(datetime.now()),
                    "sensor_type": "object_status",
                    "sensor_value": random.choice([0, 1]), #0: absence, 1: presence
                    "created_at": str(datetime.now()),
                    "auto_mode": 1,
                    "synced_flag": 0                    
                }

                battery_level = {
                    "data_id": str(uuid.uuid4()),
                    "device_id": iot_device_id,
                    "measured_at": str(datetime.now()),
                    "sensor_type": "battery_level",
                    "sensor_value": round(random.uniform(5, 80), 2),
                    "created_at": str(datetime.now()),
                    "auto_mode": 1,
                    "synced_flag": 0 
                }

                lis_data.append(object_status)
                lis_data.append(battery_level)
            else:
                pass

        else: #Gen data from Json
            if iot_device_id == con_iot_device_id:
                with open(file_name, "r") as json_file:
                    data = json.load(json_file)

                object_status_json = data.get("sensors", {}).get("object_status", None)  # Default to None if the key doesn't exist
                object_status = {
                    "data_id": str(uuid.uuid4()),
                    "device_id": iot_device_id,
                    "measured_at": str(datetime.now()),
                    "sensor_type": "object_status",
                    "sensor_value": object_status_json,
                    "created_at": str(datetime.now()),
                    "auto_mode": 0,
                    "synced_flag": 0 
                }

                battery_level_json = data.get("sensors", {}).get("battery_level", None)  # Default to None if the key doesn't exist
                battery_level = {
                    "data_id": str(uuid.uuid4()),
                    "device_id": iot_device_id,
                    "measured_at": str(datetime.now()),
                    "sensor_type": "battery_level",
                    "sensor_value": round(battery_level_json, 2),
                    "created_at": str(datetime.now()),
                    "auto_mode": 0,
                    "synced_flag": 0 
                }

                lis_data.append(object_status)
                lis_data.append(battery_level)
            else:
                pass

    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        
    return lis_data

def create_iot_config(iot_device_id):
    try:
        file_name = os.path.join(root_path, "backend", "database", "iot_local_db" , f"""{iot_device_id}.json""")
        #print(f"""DEBUG: {inspect.currentframe().f_code.co_name}() - file_name = {file_name}""")

        if not os.path.exists(file_name):
            
            # Get the current timestamp with timezone
            current_time = datetime.now(pytz.utc).isoformat()

            data = {
                "device_id": iot_device_id,
                "auto_flag": int(os.getenv("SB__GEN_DATA_MODE")),
                "sensors": {
                    "object_status": 0,
                    "battery_level": 70.00
                },
                "create_at": current_time,
                "create_by": os.getenv("SB__USER_ADMIN_ID"),
                "update_at": current_time,
                "update_by": os.getenv("SB__USER_ADMIN_ID"),
            }

            # Write data to a JSON file
            with open(file_name, "w") as json_file:
                json.dump(data, json_file, indent=4)

            print(f"""File "{file_name}" created successfully.""")
            return (True, 1)
            
        else:
            print(f"""File "{file_name}" already exists.""")
            with open(file_name, "r") as json_file:
                data = json.load(json_file)

            auto_flag = data.get("auto_flag", None) #Integer

            if auto_flag == 1:
                print(f"""Auto generate mode is online...""")
                return (True, 1)
                
            else:
                print(f"""Auto generate mode is offline!""")
                return (True, 0)
        
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return (False, 0)

# Store data in SQLite
def store_data(iot_device_id, data):

    db_filename = os.path.join(root_path, "backend", "database", "iot_local_db" , f"""{iot_device_id}.sqlite3""")
    
    # Check if the database file exists, if not, create it
    if not os.path.exists(db_filename):
        print(f"Database {db_filename} does not exist. Creating a new database.")
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        # Create the table if the database is new
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iot_data (
                data_id TEXT PRIMARY KEY,
                device_id TEXT,
                measured_at TEXT,
                sensor_type TEXT,
                sensor_value REAL,
                created_at TEXT,
                auto_mode INTERGER,
                synced_flag INTEGER                         
            );
        """)
        conn.commit()  # Commit the transaction to create the table
    else:
        # If database exists, just connect to it
        print(f"Database {db_filename} already exists. Connecting to the existing database.")
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
    
    #Loop to insert
    for row in data:
        try:
            cursor.execute(f"""
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
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?,?
                )
            """, (
                row["data_id"],
                row["device_id"],
                row["measured_at"],
                row["sensor_type"],
                row["sensor_value"],
                row["created_at"],
                row["auto_mode"],
                row["synced_flag"]
            ))
        
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}\n device_id: {row["device_id"]}, data_id: {row["data_id"]}""")
            return False
    #
    conn.commit()
    conn.close()
    print(f"""device_id: {row["device_id"]}, data_id: {row["data_id"]}, Store data successfully""")
    return True
        
# Main
def iot_generator(iot_device_id):
    time_sleep = int(os.getenv("SB__GEN_DATA_FREQUENCY"))
    while True:        
        result_iot_con, auto_mode = create_iot_config(iot_device_id)
        if result_iot_con == True:
                if auto_mode == 1:
                    data = gen_data(iot_device_id, auto_mode)
                else:
                    file_name = os.path.join(root_path, "backend", "database", "iot_local_db" , f"""{iot_device_id}.json""")
                    data = gen_data(iot_device_id, auto_mode, file_name)
                #   
                if data != []:
                    if store_data(iot_device_id, data) == True:
                        print(f"""Data generated and stored successfully!", "iot_device_id": {iot_device_id}, "data_id": {data[-1]["data_id"]}""")
                    else:
                        print(f"""Data generated and stored fail!": {iot_device_id}, "data_id": {data[-1]["data_id"]}""")
                else:
                    print(f"""Cannot generate data", "iot_device_id": {iot_device_id}""")
        else:
            print(f"""Cannot create iot configure file", "iot_device_id": {iot_device_id}""")
        #
        time.sleep(time_sleep)

