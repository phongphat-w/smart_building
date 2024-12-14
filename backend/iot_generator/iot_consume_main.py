# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sqlite3
import time
import traceback
from datetime import datetime
from multiprocessing.pool import Pool

# Third-party library imports
import psycopg2
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from dotenv import load_dotenv

# Local application imports:
#

class KafkaConsumerManager():
    def __init__(self, iot_device_id):
        self.iot_device_id = iot_device_id
        self.load_config()
        self.setup_kafka()
        self.config_log()

        # SQLite database path
        self.db_path = os.path.join(self.root_path, "backend", "database", "iot_local_db")

    def load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, "", ".env"))
        self.SB_KAFKA_HOST = os.getenv("SB_KAFKA_HOST")
        self.SB_KAFKA_PORT = os.getenv("SB_KAFKA_PORT")
        self.SB_KAFKA_CONSUMER_GROUP = os.getenv("SB_KAFKA_CONSUMER_GROUP")
        self.SB_KAFKA_CONSUMER_TOPIC = os.getenv("SB_KAFKA_CONSUMER_TOPIC")
        self.SB_TIMESCALEDB_DB_HOST = os.getenv("SB_TIMESCALEDB_DB_HOST")
        self.SB_TIMESCALEDB_DB_PORT = os.getenv("SB_TIMESCALEDB_DB_PORT")
        self.SB_TIMESCALEDB_DB_NAME = os.getenv("SB_TIMESCALEDB_DB_NAME")
        self.SB_TIMESCALEDB_DB_USER = os.getenv("SB_TIMESCALEDB_DB_USER")
        self.SB_TIMESCALEDB_DB_PASSWORD = os.getenv("SB_TIMESCALEDB_DB_PASSWORD")
        self.SB_KAFKA_DATA_FREQUENCY = int(os.getenv("SB_KAFKA_DATA_FREQUENCY"))

    def setup_kafka(self):
        self.consumer_config = {
            "bootstrap.servers": f"{self.SB_KAFKA_HOST}:{self.SB_KAFKA_PORT}",
            "group.id": self.SB_KAFKA_CONSUMER_GROUP,
            "auto.offset.reset": "earliest",
        }
        # Kafka Producer and Consumer instances
        self.producer = Producer({"bootstrap.servers": f"{self.SB_KAFKA_HOST}:{self.SB_KAFKA_PORT}"})
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([self.SB_KAFKA_CONSUMER_TOPIC])

    def config_log(self):
        log_dir = os.path.join(self.root_path, "logs")
        os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
        log_file_path = os.path.join(log_dir, "iot_gen.log")

        # Configure TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(
            log_file_path, 
            when="midnight",    # Rotate at midnight
            interval=1,         # Interval of 1 day
            backupCount=500     # Keep the last 500 log files
        )
        
        # Add a datetime format to the rotated log files
        handler.suffix = "%Y-%m-%d"

        # Configure logging
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[handler]  # Use the TimedRotatingFileHandler
        )
        self.logger = logging.getLogger(__name__)

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
                    print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
                    self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
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
            conn.close()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            if conn: conn.close()
            return False

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

    def get_iot_info(self):
        conn = None
        try:
            conn = self.get_server_conn()
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
                conn.close()
                return []
        except Exception as e:
            if conn: conn.close()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return []

    def fetch_unsynced_local_db(self):
        conn = None
        try:
            iot_info = self.get_iot_info()
            
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
        except Exception as e:
            if conn: conn.close()
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return []    

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
            self.producer.produce(self.SB_KAFKA_CONSUMER_TOPIC, value=serialized_data)
            self.producer.flush()

            print(f"Produced {len(data)} records to Kafka topic {self.SB_KAFKA_CONSUMER_TOPIC}.")
            self.logger.info(f"Produced {len(data)} records to Kafka topic {self.SB_KAFKA_CONSUMER_TOPIC}.")

            return True

            
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
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
                print(f"{inspect.currentframe().f_code.co_name}(): Error - Invalid Kafka message format: {kafka_data}")
                self.logger.error(f"{inspect.currentframe().f_code.co_name}(): Error - Invalid Kafka message format: {kafka_data}")
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

# def consume_iot_data_main()
if __name__ == "__main__":  
    iot_device_ids = [
        "7c84b98d-8f69-4959-ac5b-1b2743077151",  # Smart thermostats
        "080d460f-e54c-4262-a4ac-a3d42c40cbd5",  # Demand-Controlled Ventilation (DCV)
        "c0ec3c70-b76f-45e0-9297-8b5a4a462a47", #Smart bulbs and LED lights
        "f531b9c1-c46a-42c4-989d-1d5be315f6a6", #Smart meters
        "96b38698-d9ad-4355-807f-5580397471a1", #Presence sensors
        "69b29098-c768-423e-ac2e-cc443e18f8a9", #Automated blinds or shades
    ]
    with Pool(processes=10) as pool:  # Limit to 10 concurrent processes
        pool.map(run_consume, iot_device_ids)

    print("Muti-consumers have completed execution.")