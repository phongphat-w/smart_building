# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import datetime
import hashlib
import inspect
import json
import logging
import os
import sqlite3
import sys
import time
import traceback
from logging.handlers import TimedRotatingFileHandler
from multiprocessing.pool import Pool

# Third-party library imports
import psycopg2
import pytz
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from dotenv import load_dotenv

# Local application imports:
# from iot_get_info import IotInfo
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from backend.iot_generator.iot_utils.iot_get_info import IotInfo # Absolute import
from backend.logging.system_logging import IotLogging

class KafkaConsumerManager():
    def __init__(self, iot_device_id):
        self.__load_config()
        self.setup_kafka()
        self.iot_device_id = iot_device_id
        self.log = IotLogging(self.SB_IOT_CONSUME_DATA_LOG_FILE)

        # SQLite database path
        self.db_path = os.path.join(self.root_path, "database", "iot_local_db")

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # print("DEBUG: self.root_path = " + self.root_path)
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))
        self.SB_PROJECT_STD_TIMEZONE = os.getenv("SB_PROJECT_STD_TIMEZONE")
        self.SB_KAFKA_HOST = os.getenv("SB_KAFKA_HOST")
        self.SB_KAFKA_PORT = os.getenv("SB_KAFKA_PORT")
        self.SB_IOT_CONSUME_DATA_LOG_FILE = os.getenv("SB_IOT_CONSUME_DATA_LOG_FILE")
        self.SB_KAFKA_CONSUMER_GROUP = os.getenv("SB_KAFKA_CONSUMER_GROUP")
        self.SB_KAFKA_TOPIC = os.getenv("SB_KAFKA_TOPIC")
        self.SB_TIMESCALEDB_DB_HOST = os.getenv("SB_TIMESCALEDB_DB_HOST")
        self.SB_TIMESCALEDB_DB_PORT = os.getenv("SB_TIMESCALEDB_DB_PORT")
        self.SB_TIMESCALEDB_DB_NAME = os.getenv("SB_TIMESCALEDB_DB_NAME")
        self.SB_TIMESCALEDB_DB_USER = os.getenv("SB_TIMESCALEDB_DB_USER")
        self.SB_TIMESCALEDB_DB_PASSWORD = os.getenv("SB_TIMESCALEDB_DB_PASSWORD")
        self.SB_KAFKA_DATA_FREQUENCY = int(os.getenv("SB_KAFKA_DATA_FREQUENCY"))
        self.SB_KAFKA_COMPRESSION = os.getenv("SB_KAFKA_COMPRESSION")

        # print("DEBUG: load_config() - self.SB_KAFKA_TOPIC = " + self.SB_KAFKA_TOPIC)

    def setup_kafka(self):
        # Kafka consumer instances
        self.consumer_config = {
            "bootstrap.servers": f"{self.SB_KAFKA_HOST}:{self.SB_KAFKA_PORT}",
            "group.id": self.SB_KAFKA_CONSUMER_GROUP,
            "auto.offset.reset": "earliest",
        }
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([self.SB_KAFKA_TOPIC])

        # Kafka Producer instances 
        producer_config = {
            "bootstrap.servers": f"{self.SB_KAFKA_HOST}:{self.SB_KAFKA_PORT}",
            "compression.type": self.SB_KAFKA_COMPRESSION,
            "batch.num.messages": 1000,
        }        
        self.producer = Producer(producer_config)

    def get_server_conn(self):
        retries = 3
        for attempt in range(retries):
            try:
                conn = psycopg2.connect(
                    host=self.SB_TIMESCALEDB_DB_HOST,
                    port=self.SB_TIMESCALEDB_DB_PORT,
                    dbname=self.SB_TIMESCALEDB_DB_NAME,
                    user=self.SB_TIMESCALEDB_DB_USER,
                    password=self.SB_TIMESCALEDB_DB_PASSWORD,
                )
                return conn
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
                    print(error_msg)
                    self.logger.error(error_msg)
                    return None

    def insert_centralized_db(self, conn, data):
        try:
            print(f"{inspect.currentframe().f_code.co_name}(): Info - {data}")
            # Convert list of dictionaries to list of tuples for executemany
            data_values = [
                (
                    record["device_id"],
                    record["client_id"],
                    record["account_id"],
                    record["measured_at"],
                    record["sensor_type"],
                    record["sensor_value"],
                    record["created_at_iot"],
                )
                for record in data
            ]
            
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.executemany(
                """
                INSERT INTO iot_data (
                    device_id, client_id, account_id, measured_at, sensor_type, sensor_value, created_at_iot
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                data_values,
            )
            conn.commit()
            print(f"Data inserted into centralized database successfully for {len(data)} records.")
            self.logger.info(f"Inserted {len(data)} records into TimescaleDB.")
            return True
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            if conn: conn.rollback()    
            return False
        finally:
            if conn: conn.close()

    def update_local_db(self): #SQLite
        conn = None
        try:
            conn = sqlite3.connect( os.path.join(self.db_path, f"{self.iot_device_id}.sqlite3") )
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("UPDATE iot_data  SET synced_flag = 1 WHERE synced_flag = 0")
            cursor.execute("DELETE FROM iot_data WHERE synced_flag = 1")
            conn.commit()
            print(f"Updated synced_flag to 1 and deleted synced records for device {self.iot_device_id}.")
        except Exception as e:
            if conn: conn.rollback()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
        finally:
            if conn: conn.close()


    def fetch_unsynced_local_db(self):
        conn = None
        try:
            iot = IotInfo(self.iot_device_id)
            iot_info = iot.get_iot_info()
            
            if iot_info != "[]":
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
                        "client_id": iot_info[0]["client_id"],
                        "account_id": iot_info[0]["account_id"],
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
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            if conn: conn.close()
            return []    

    def get_partition_key(self):
        """
        Hash the device_id to create a consistent partition key.
        """
        hashed_key = hashlib.md5(self.iot_device_id.encode()).hexdigest()
        partition_key = int(hashed_key, 16) # Convert hash to integer for partition calculations
        return str(partition_key)  # Kafka requires a string key
    
    def delivery_report(self, err, msg):
        if err:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    
    def produce_to_kafka(self, data): # Produce unsynced data to Kafka
        """
        Produce multiple records to Kafka.
        
        Args:
            data (list): List of records (dictionaries) to produce to Kafka.
        
        Returns:
            bool: True if all records are successfully produced, False otherwise.
        """
        try:
            if not data:
                print("No data to produce to Kafka.")
                self.logger.info("No data to produce to Kafka.")
                return True

            # Serialize all records into a single JSON array
            serialized_data = json.dumps(data)
            # print(f"{inspect.currentframe().f_code.co_name}(): Info - {serialized_data}")

            # Produce the serialized data to Kafka
            self.producer.produce(self.SB_KAFKA_TOPIC, key=self.get_partition_key(), value=serialized_data, callback=self.delivery_report())
            self.producer.flush()

            print(f"Produced {len(data)} records to Kafka topic {self.SB_KAFKA_TOPIC}.")
            self.logger.info(f"Produced {len(data)} records to Kafka topic {self.SB_KAFKA_TOPIC}.")

            return True
            
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            return False
        
    def get_unsynced_data(self): # Start ingest data from SQLite

        unsynced_data = self.fetch_unsynced_local_db()
        if unsynced_data:
            self.produce_to_kafka(unsynced_data) #Produce to Kafka               
        else:
            print(f"No unsynced data for device {self.iot_device_id}.")

    def insert_server_db(self, msg):
        """
        Processes a Kafka message containing multiple records and inserts them into the server database.

        Args:
            msg: The Kafka message received by the consumer.

        Returns:
            bool: True if all records are processed successfully, False otherwise.
        """
        try:
            # Deserialize the message into a list of records
            kafka_data = json.loads(msg.value().decode("utf-8"))

            # Ensure kafka_data is a list
            if isinstance(kafka_data, dict):  # Single record case
                kafka_data = [kafka_data]  # Convert to list for consistency
            elif not isinstance(kafka_data, list):  # Invalid case
                error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - Invalid Kafka message format: {kafka_data} - {e}\n{traceback.format_exc()}"""
                print(error_msg)
                self.logger.error(error_msg)
                return False

            # kafka_data is list
            conn = self.get_server_conn()
            if conn:
                # Insert all records into the centralized DB
                if self.insert_centralized_db(conn, kafka_data):  # Pass the list directly
                    print(f"Successfully processed {len(kafka_data)} records.")
                    self.logger.info(f"Successfully processed {len(kafka_data)} records.")
                    return True
                else:
                    print(f"{inspect.currentframe().f_code.co_name}(): Error - Failed to insert records into the database.")
                    self.logger.errorf(f"{inspect.currentframe().f_code.co_name}(): Error - Failed to insert records into the database.")
                    return False
            else:
                print(f"{inspect.currentframe().f_code.co_name}(): Error - Could not establish a database connection.")
                self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - Could not establish a database connection.")
                return False
           
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return False

    def consume_kafka_main(self):
        try:
            while True:
                self.get_unsynced_data()

                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Kafka error: {msg.error()}")
                    continue

                if self.insert_server_db(msg):
                    self.update_local_db()

                time.sleep(self.SB_KAFKA_DATA_FREQUENCY)

        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
        finally:
            self.consumer.close()

#=======================================
def run_consume(iot_device_id):
    consumer = KafkaConsumerManager(iot_device_id)
    consumer.consume_kafka_main()

#def consume_iot_data_main(): 
if __name__ == "__main__":
    """
    Creates multiple Kafka consumers for a list of IoT device IDs
    and runs them in parallel using a process pool.
    """
    iot_device_ids = [
        "7c84b98d-8f69-4959-ac5b-1b2743077151",  # Smart thermostats
        "080d460f-e54c-4262-a4ac-a3d42c40cbd5",  # Demand-Controlled Ventilation (DCV)
        "c0ec3c70-b76f-45e0-9297-8b5a4a462a47", #Smart bulbs and LED lights
        "f531b9c1-c46a-42c4-989d-1d5be315f6a6", #Smart meters
        "96b38698-d9ad-4355-807f-5580397471a1", #Presence sensors
        "69b29098-c768-423e-ac2e-cc443e18f8a9", #Automated blinds or shades
    ]
    with Pool(processes=100) as pool:  # Limit concurrent processes
        pool.map(run_consume, iot_device_ids)

    # print("Muti-consumers have completed execution.")