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
import traceback

class KafkaConsumer():
    def __init__(self, iot_device_id):
        self.iot_device_id = iot_device_id
        self.root_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

        # Load environment variables
        load_dotenv(dotenv_path=os.path.join(self.root_path, "", ".env"))

        # Kafka Consumer configuration
        self.consumer_config = {
            #"bootstrap.servers": f"{os.getenv('SB_KAFKA_HOST')}:{os.getenv('SB_KAFKA_PORT')}",
            "bootstrap.servers":"172.18.0.7:9092", #local docker
            # "bootstrap.servers": "kafka:9092", #local docker
            "group.id": "iot-consumer-group",
            "auto.offset.reset": "earliest",
        }

        # Kafka Consumer instance
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe(["iot_data_topic"])

        # SQLite database path
        self.db_path = os.path.join(self.root_path, "backend", "database", "iot_local_db")

    def get_timescaledb_connection(self):
        try:
            conn = psycopg2.connect(
                host=os.getenv("SB_TIMESCALEDB_DB_HOST"),
                port=os.getenv("SB_TIMESCALEDB_DB_PORT"),
                dbname=os.getenv("SB_TIMESCALEDB_DB_NAME"),
                user=os.getenv("SB_TIMESCALEDB_DB_USER"),
                password=os.getenv("SB_TIMESCALEDB_DB_PASSWORD"),
            )
            return conn
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return None

    def insert_into_timescaledb(self, conn, data):
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN;")

            data_values = [
                (
                    data["device_id"],
                    data["client_id"],
                    data["account_id"],
                    data["measured_at"],
                    data["sensor_type"],
                    data["sensor_value"],
                    data["created_at_iot"],
                )
            ]

            cursor.executemany(
                """
                INSERT INTO iot_data (
                    device_id, client_id, account_id, measured_at, sensor_type, sensor_value, created_at_iot
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                data_values,
            )

            conn.commit()
            print(f"Data inserted into TimescaleDB successfully for {len(data)} records.")
            return True
        except Exception as e:
            conn.rollback()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            return False
        finally:
            conn.close()

    def update_and_delete_from_sqlite(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN;")

            cursor.execute(
                """
                UPDATE iot_data
                SET synced_flag = 1
                WHERE synced_flag = 0
                """
            )

            cursor.execute(
                """
                DELETE FROM iot_data
                WHERE synced_flag = 1
                """
            )

            conn.commit()
            print(f"Updated synced_flag to 1 and deleted synced records for device {self.iot_device_id}.")
        except Exception as e:
            conn.rollback()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            raise

    def get_iot_info(self):
        conn = self.get_timescaledb_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                SELECT a.account_id, c.client_id, c.client_name, d.country_name, d.time_zone
                FROM iot_device a
                INNER JOIN account b ON a.account_id = b.account_id
                INNER JOIN client c ON b.client_id = c.client_id
                INNER JOIN country d ON c.country_id = d.country_id
                WHERE a.iot_device_id = '{self.iot_device_id}'
                """
            )
            row = cursor.fetchall()
            conn.close()
            return row
        else:
            return []

    def fetch_unsynced_data_from_sqlite(self):
        iot_info = self.get_iot_info(self.iot_device_id)

        if iot_info:
            db_filename = os.path.join(self.db_path, f"{self.iot_device_id}.sqlite3")
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT data_id, device_id, measured_at, sensor_type, sensor_value, created_at, synced_flag
                FROM iot_data
                WHERE synced_flag = 0
                """
            )
            rows = cursor.fetchall()

            data = [
                {
                    "device_id": row[1],
                    "client_id": iot_info[0][1],
                    "account_id": iot_info[0][0],
                    "measured_at": row[2],
                    "sensor_type": row[3],
                    "sensor_value": row[4],
                    "created_at_iot": row[5],
                }
                for row in rows
            ]

            conn.close()
            return data
        else:
            return []

    def consume_push(self):
        time_sleep = int(os.getenv("SB_KAFKA_DATA_FREQUENCY", 10))

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Kafka error: {msg.error()}")
                    continue

                unsynced_data = self.fetch_unsynced_data_from_sqlite(self.iot_device_id)
                if unsynced_data:
                    conn = self.get_timescaledb_connection()
                    if conn:
                        for data in unsynced_data:
                            self.insert_into_timescaledb(conn, data)

                        sqlite_conn = sqlite3.connect( os.path.join(self.db_path, f"{self.iot_device_id}.sqlite3") )
                        self.update_and_delete_from_sqlite(sqlite_conn, self.iot_device_id)
                        sqlite_conn.close()
                else:
                    print(f"No unsynced data for device {self.iot_device_id}.")

                time.sleep(time_sleep)
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
        finally:
            self.consumer.close()


#=======================================
def run_thermostats():
    iot_device_id = "7c84b98d-8f69-4959-ac5b-1b2743077151"  # Smart thermostats
    iot1 = KafkaConsumer(iot_device_id) 
    iot1.consume_push()

def run_dem_con_ven():
    iot_device_id = "080d460f-e54c-4262-a4ac-a3d42c40cbd5"  # Demand-Controlled Ventilation (DCV)
    iot2 = KafkaConsumer(iot_device_id) 
    iot2.consume_push()

def run_bulb_led():
    iot_device_id = "c0ec3c70-b76f-45e0-9297-8b5a4a462a47" #Smart bulbs and LED lights
    iot3 = KafkaConsumer(iot_device_id) 
    iot3.consume_push()

def run_smart_meter():
    iot_device_id = "f531b9c1-c46a-42c4-989d-1d5be315f6a6" #Smart meters
    iot4 = KafkaConsumer(iot_device_id) 
    iot4.consume_push()

def run_presence():
    iot_device_id = "96b38698-d9ad-4355-807f-5580397471a1" #Presence sensors
    iot5 = KafkaConsumer(iot_device_id) 
    iot5.consume_push()

def run_blinds_shades():
    iot_device_id = "69b29098-c768-423e-ac2e-cc443e18f8a9" #Automated blinds or shades
    iot6 = KafkaConsumer(iot_device_id) 
    iot6.consume_push()

# def consume_iot_data_main():
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