# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import logging
import os
import subprocess
import traceback
from logging.handlers import TimedRotatingFileHandler

# Third-party library imports
from dotenv import load_dotenv

# Local application imports:
#

class KafkaTopicManager():
    def __init__(self):
        self.__load_config()
        self.config_log()

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        print("DEBUG: self.root_path = ", self.root_path)

        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))
        self.SB_KAFKA_HOST = os.getenv("SB_KAFKA_HOST")
        self.SB_KAFKA_PORT = os.getenv("SB_KAFKA_PORT")
        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE")
        self.SB_KAFKA_TOPIC = os.getenv("SB_KAFKA_TOPIC")
        self.SB_KAFKA_CONTAINER_NAME = os.getenv("SB_KAFKA_CONTAINER_NAME")
        self.SB_KAFKA_EXEC_PATH = os.getenv("SB_KAFKA_EXEC_PATH")

        self.bootstrap_server = f"{self.SB_KAFKA_HOST}:{self.SB_KAFKA_PORT}"     

    def config_log(self):
        log_dir = os.path.join(self.root_path, "logs")
        os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
        log_file_path = os.path.join(log_dir, f"{self.SB_IOT_GEN_DATA_LOG_FILE}.log")

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

    def create_topic(self, replication_factor=1, partitions=10):
        """
        Create a Kafka topic using the Kafka CLI.

        Args:
            topic_name (str): Name of the Kafka topic to create.
            replication_factor (int): Number of replicas for the topic.
            partitions (int): Number of partitions for the topic.

        Returns:
            str: Output from the Kafka topic creation command.
        """
        try:
            # Define the Docker exec command to run inside the Kafka container
            command = [
                "docker", "exec", "-i", f"{self.SB_KAFKA_CONTAINER_NAME}",  # Run command inside Kafka container
                f"{self.SB_KAFKA_EXEC_PATH}/kafka-topics", #.sh
                "--create",
                f"--bootstrap-server={self.bootstrap_server}",
                f"--replication-factor={replication_factor}",
                f"--partitions={partitions}",
                f"--topic={self.SB_KAFKA_TOPIC}",
            ]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"""Topic "{self.SB_KAFKA_TOPIC}" created successfully.""")
            return result.stdout
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            logging.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return e

    def list_topics(self):
        """
        List all Kafka topics using the Kafka CLI.

        Returns:
            str: Output from the Kafka topic listing command.
        """
        try:
            # Define the Docker exec command to run inside the Kafka container
            command = [
                "docker", "exec", "-i", f"{self.SB_KAFKA_CONTAINER_NAME}",  # Run command inside Kafka container
                f"{self.SB_KAFKA_EXEC_PATH}/kafka-topics", #.sh
                "--list",
                f"--bootstrap-server={self.bootstrap_server}",
            ]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Kafka topics listed successfully.")
            return result.stdout
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            logging.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return e

    def delete_topic(self, topic_name):
        """
        Delete a Kafka topic using the Kafka CLI.

        Args:
            topic_name (str): Name of the Kafka topic to delete.

        Returns:
            str: Output from the Kafka topic deletion command.
        """
        try:# Define the Docker exec command to run inside the Kafka container
            command = [
                "docker", "exec", "-i", f"{self.SB_KAFKA_CONTAINER_NAME}",  # Run command inside Kafka container
                f"{self.SB_KAFKA_EXEC_PATH}/kafka-topics", #.sh
                "--delete",
                f"--bootstrap-server={self.bootstrap_server}",
                f"--topic={topic_name}",
            ]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"""Topic "{topic_name}" deleted successfully.""")
            return result.stdout
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            logging.error(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
            return e


if __name__ == "__main__":
    manager = KafkaTopicManager()
    topic_creation_output = manager.create_topic(replication_factor=1, partitions=50)
    print(topic_creation_output)

    # List all topics
    topics_list = manager.list_topics()
    print(f"Available topics:\n{topics_list}")

    # Delete a topic
    # topic_deletion_output = manager.delete_topic(topic_name=f"{topics_list}")
    # print(topic_deletion_output)

