# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import json
import os
import sys
import traceback
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv

# Third-party library imports
import pytz

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.iot_generator.generation.iot_device_master import IotDeviceMaster # Absolute import
from backend.iot_generator.generation.iot_sensor_master import IotSensorMaster # Absolute import
from backend.iot_generator.iot_utils.iot_get_info import IotInfo # Absolute import
from backend.logging.system_logging import IotLogging # Absolute import

class IotDeviceStruct:
    def __init__(self, iot_device_id):
        self.__load_config()
        self.iot_device_id = iot_device_id
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)
        self.__initial_config()

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 
        self.SB_PROJECT_STD_TIMEZONE = os.getenv("SB_PROJECT_STD_TIMEZONE") 
        self.SB_GEN_DATA_MODE = int(os.getenv("SB_GEN_DATA_MODE"))

    def __initial_config(self):
        try:
            admin_info = IotInfo(self.iot_device_id).get_admin_info()
            if not admin_info:
                error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - Cannot create configuration file for IOT device id: {self.iot_device_id}"""
                print(error_msg)
                self.log.error(error_msg)
                return (False, 1)
            
            # Get the current timestamp with timezone
            #YYYY-MM-DDTHH:MM:SS.mmmmmm+00:00, 2024-12-18T14:35:22.123456+00:00
            current_time = datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE)).isoformat()
            if self.iot_device_id == IotDeviceMaster.get_device_id("thermostats"):
                sensors = defaultdict(lambda: None, {
                    "temperature": IotSensorMaster.get_sensor_default("temperature")
                })
            else:
                sensors = defaultdict(lambda: None)

            # Default value for battery level
            sensors["battery_level"] = IotSensorMaster.get_sensor_default("battery_level")

            # Initialize the data with default values
            self.__data = defaultdict(lambda: None, {
                "device_id": self.iot_device_id,
                "auto_flag": self.SB_GEN_DATA_MODE,
                "sensors": sensors,
                "create_at": current_time,
                "create_by": admin_info[0]["id"],
                "update_at": current_time,
                "update_by": admin_info[0]["id"]
            })            
            
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - Cannot create configuration file for IOT device id: {self.iot_device_id}\n{traceback.format_exc()}"""
            print(error_msg)
            self.log.logger.error(error_msg)
            return (False, 1)

    def get_iot_device_struct(self):
        """
        Returns the current state of the data structure.
        """
        return self.__data
    
    def set_iot_device_struct(self, data_dict):
        """
        Updates the data structure with the values from the provided dictionary.
        
        Args:
            data_dict (dict): A dictionary with the new values to update.
        """
        for key, value in data_dict.items():
            if key in self.__data:
                if isinstance(self.__data[key], dict) and isinstance(value, dict):
                    # Handle nested dictionaries
                    self.__data[key].update(value)
                else:
                    self.__data[key] = value
            else:
                print(f"Warning: {key} is not a valid field.")