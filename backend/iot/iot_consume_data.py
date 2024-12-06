import json
import psycopg2
import sqlite3
from confluent_kafka import Consumer, KafkaException, KafkaError
from datetime import datetime
import os
import time
from dotenv import load_dotenv
import inspect
import multiprocessing

root_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

# Load environment variables from .env file
load_dotenv(dotenv_path = os.path.join(root_path, "", ".env"))

# Define Kafka Consumer configuration
consumer_config = {
    "bootstrap.servers": f"""{os.getenv("SB__KAFKA_HOST")}:{os.getenv("SB__KAFKA_PORT")}""",  # Kafka server
    "group.id": "iot-consumer-group",
    "auto.offset.reset": "earliest"  # Start from the earliest message
}

# Create Kafka Consumer instance
consumer = Consumer(consumer_config)

# SQLite database path
DB_PATH = os.path.join(root_path, "backend", "database", "iot_local_db")
# Connect to TimescaleDB
def get_timescaledb_connection():
    try:
        conn = psycopg2.connect(
            host = os.getenv("SB__TIMESCALEDB_DB_HOST"),
            port = os.getenv("SB__TIMESCALEDB_DB_PORT"),
            dbname = os.getenv("SB__TIMESCALEDB_DB_NAME"),
            user = os.getenv("SB__TIMESCALEDB_DB_USER"),
            password = os.getenv("SB__TIMESCALEDB_DB_PASSWORD")            
        )
        return conn
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return None

# Insert data into TimescaleDB
def insert_into_timescaledb(conn, data):

    #print(f"""data_list = {data_list}""")

    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        
        # Prepare the data to be inserted
        data_values = [
            (
                data["device_id"],
                data["client_id"],
                data["account_id"],
                data["measured_at"],
                data["sensor_type"],
                data["sensor_value"],
                data["created_at_iot"]
            )
        ]

        # Insert multiple records at once using executemany
        cursor.executemany("""
            INSERT INTO iot_data (
                device_id, client_id, account_id, measured_at, sensor_type, sensor_value, created_at_iot
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, data_values
        )
        
        # Commit the transaction
        conn.commit()
        print(f"Data inserted into TimescaleDB successfully for {len(data)} records.")
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return False


# Update "synced_flag" and delete records from SQLite
def update_and_delete_from_sqlite(conn, iot_device_id):
    cursor = conn.cursor()

    try:
        # Start a transaction in SQLite
        cursor.execute("BEGIN;")

        # Update "synced_flag" to 1 for records that have been successfully synced
        cursor.execute("""
            UPDATE iot_data
            SET synced_flag = 1
            WHERE synced_flag = 0
            """
        )

        # Delete records where "synced_flag = 1"
        cursor.execute("""
            DELETE FROM iot_data
            WHERE synced_flag = 1
            """
        )

        # Commit the transaction
        conn.commit()
        print(f"Updated synced_flag to 1 and deleted synced records for device {iot_device_id}.")
    except Exception as e:
        conn.rollback()
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        raise

def get_iot_info(iot_device_id):
    timescale_conn = get_timescaledb_connection()
    if timescale_conn:
        cursor = timescale_conn.cursor()
        cursor.execute(f"""
            Select a.account_id::char(36), c.client_id::char(36), c.client_name, d.country_name, d.time_zone
            From iot_device a
            Inner Join account b On a.account_id = b.account_id::char(36)
            Inner Join client c On b.client_id = c.client_id::char(36)
            Inner Join country d On c.country_id = d.country_id
            Where a.iot_device_id::char(36) = '{iot_device_id}'
            """
        )
        row = cursor.fetchall()
        return row
    else:
        return []

# Fetch unsynced data from SQLite
def fetch_unsynced_data_from_sqlite(iot_device_id):
    #Postgres
    iot_info = get_iot_info(iot_device_id)

    if iot_info != []:

        #SQLite
        db_filename = os.path.join(DB_PATH, f"{iot_device_id}.sqlite3")
        #print(f"""fetch_unsynced_data_from_sqlite(), db_filename = {db_filename}""")
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Fetch records where synced_flag is 0 (unsynced)
        cursor.execute("""SELECT 
                        data_id,
                        device_id,
                        measured_at,
                        sensor_type,
                        sensor_value,
                        created_at,
                        synced_flag  FROM iot_data 
                        WHERE synced_flag = 0
                       """
        )
        rows = cursor.fetchall()

        # Prepare data to be sent to Kafka
        data = []
        for row in rows:
            data.append({
                #"data_id": row[0],
                "device_id": row[1],
                "client_id": iot_info[0][1],
                "account_id": iot_info[0][0],
                "measured_at": row[2],
                "sensor_type": row[3],
                "sensor_value": row[4],
                "created_at_iot": row[5]
            })

        conn.close()
        return data
    else:
        return []

# Main
def consume_and_send_to_kafka(iot_device_id):
    consumer.subscribe(["iot_data_topic"])  # Subscribe to the Kafka topic
    time_sleep = int(os.getenv("SB__KAFKA_DATA_FREQUENCY"))
    
    try:
        while True:
            iot_device_id = iot_device_id
            unsynced_data = fetch_unsynced_data_from_sqlite(iot_device_id)
            if unsynced_data:
                # Connect to TimescaleDB
                timescale_conn = get_timescaledb_connection()
                if timescale_conn:
                    for data in unsynced_data:
                        # Insert the data into TimescaleDB
                        if insert_into_timescaledb(timescale_conn, data):
                            # Update and delete records from SQLite (perform in the same transaction)
                            sqlite_conn = sqlite3.connect(os.path.join(DB_PATH, f"{iot_device_id}.sqlite3"))
                            update_and_delete_from_sqlite(sqlite_conn, iot_device_id)
                            sqlite_conn.close()
            else:
                print(f"""Data is synced successfully / No data to be synced, iot_device_id: {iot_device_id}""")
            #
            time.sleep(time_sleep)
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
    finally:
        consumer.close()        

def run_thermostats():
    iot_device_id = "7c84b98d-8f69-4959-ac5b-1b2743077151"  # Smart thermostats
    consume_and_send_to_kafka(iot_device_id)

def run_dem_con_ven():
    iot_device_id = "080d460f-e54c-4262-a4ac-a3d42c40cbd5"  # Demand-Controlled Ventilation (DCV)
    consume_and_send_to_kafka(iot_device_id)

def run_bulb_led():
    iot_device_id = "c0ec3c70-b76f-45e0-9297-8b5a4a462a47" #Smart bulbs and LED lights
    consume_and_send_to_kafka(iot_device_id)

def run_smart_meter():
    iot_device_id = "f531b9c1-c46a-42c4-989d-1d5be315f6a6" #Smart meters
    consume_and_send_to_kafka(iot_device_id)

def run_presence():
    iot_device_id = "96b38698-d9ad-4355-807f-5580397471a1" #Presence sensors
    consume_and_send_to_kafka(iot_device_id)

def run_blinds_shades():
    iot_device_id = "69b29098-c768-423e-ac2e-cc443e18f8a9" #Automated blinds or shades
    consume_and_send_to_kafka(iot_device_id)

if __name__ == "__main__":

    process_thermostats = multiprocessing.Process(target=run_thermostats)
    process_dem_con_ven = multiprocessing.Process(target=run_dem_con_ven)
    process_bulb_led = multiprocessing.Process(target=run_bulb_led)
    process_smart_meter = multiprocessing.Process(target=run_smart_meter)
    process_presence = multiprocessing.Process(target=run_presence)
    process_blinds_shades = multiprocessing.Process(target=run_blinds_shades)

    process_thermostats.start()
    process_dem_con_ven.start()
    process_bulb_led.start()
    process_smart_meter.start()
    process_presence.start()
    process_blinds_shades.start()

    process_thermostats.join()
    process_dem_con_ven.join()
    process_bulb_led.join()
    process_smart_meter.join()
    process_presence.join()
    process_blinds_shades.join()

    print("Muti-consumers have completed execution.")