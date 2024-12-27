# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import logging
import os
import sys
import traceback
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# Third-party library imports
import pytz  # To handle time zones
import requests  # To send logs to Loki via HTTP

# Local application imports

# Private class
class __CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None): 
        super().__init__(fmt, datefmt)
        self.timezone = pytz.timezone("UTC") #Use UTC for overall project, convert to local when display

    def formatTime(self, record, datefmt=None):
        utc_time = datetime.fromtimestamp(record.created, pytz.utc)
        localized_time = utc_time.astimezone(self.timezone)

        if datefmt:
            return localized_time.strftime(datefmt)
        else:
            return localized_time.strftime("%Y-%m-%d %H:%M:%S")

# Custom LokiHandler to send logs to Loki
class __LokiHandler(logging.Handler):
    def __init__(self, loki_url):
        super().__init__()
        self.loki_url = loki_url

    def emit(self, record):
        log_entry = self.format(record)
        try:
            response = requests.post(self.loki_url, json={
                "streams": [{
                    "stream": {
                        "job": "iot-logs"
                    },
                    # timestamp represents seconds since the Unix epoch (1970-01-01 00:00:00 UTC)
                    "values": [[str(int(record.created * 1000)), log_entry]]  # Convert timestamp to ms
                }]
            })
            response.raise_for_status()
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")

# Local application imports
class IotLogging():
    def __init__(self, log_file, loki_url="http://localhost:3100/api/prom/push"):
        self.log_file = log_file
        self.loki_url = loki_url

        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

        self.logger = None # Will be used by log_message()
        self.log_message()  # Make sure log_message() is called

    def log_message(self):
        try:
            if self.project_root not in sys.path:
                sys.path.insert(0, self.project_root)

            log_dir = os.path.join(self.project_root, "logs")
            os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists, and not raise if existing

            log_file_path = os.path.join(log_dir, f"{self.log_file}.log")

            # Configure TimedRotatingFileHandler
            file_handler = TimedRotatingFileHandler(
                log_file_path,
                when="midnight",    # Rotate at midnight
                interval=1,         # Interval of 1 day
                backupCount=366*3   # Keep the last X log files (3 years)
            )

            # Add a datetime format to the rotated log files
            file_handler.suffix = "%Y-%m-%d"

            # Create a custom formatter with a timezone and time format
            formatter = __CustomFormatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)

            # Create Loki handler to send logs to Loki
            loki_handler = __LokiHandler(self.loki_url)
            loki_handler.setFormatter(formatter) 

            # Configure logging with the custom handler
            logging.basicConfig(
                level=logging.ERROR,
                #handlers=[file_handler, file_handler]
                handlers=[file_handler]
            )

            # Create the logger
            self.logger = logging.getLogger(__name__)
            
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}")
