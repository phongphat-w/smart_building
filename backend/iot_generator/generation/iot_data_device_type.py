# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import json
import os
import random
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Third-party library imports
import pytz

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from backend.iot_generator.generation.iot_data_device_struct import IotDataDeviceStruct # Absolute import
from backend.logging.system_logging import IotLogging # Absolute import

class IotDataDeviceType():
    def __init__(self, iot_device_id, mode_id):
        self.__load_config()
        self.iot_device_id = iot_device_id
        self.mode_id = mode_id
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)
    
    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 
        self.SB_PROJECT_STD_TIMEZONE = os.getenv("SB_PROJECT_STD_TIMEZONE")
        self.SB_IOT_GEN_DATA_ERROR_VALUE = os.getenv("SB_IOT_GEN_DATA_ERROR_VALUE") 

    def __get_sensor_data(self, sensor_type):
        """
        General method to retrieve sensor data based on sensor type.        
        """
        try:
            iot_device = IotDataDeviceStruct()
            data = iot_device.get_iot_data_struct()

            data_temp = {}
            current_time = datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE)).isoformat()
            data_temp["data_id"] = str(uuid.uuid4()).join("-").join(self.iot_device_id.split("-")[0])  # 36 + 9 = 45
            data_temp["device_id"] = self.iot_device_id
            data_temp["measured_at"] = current_time
            data_temp["sensor_type"] = sensor_type
            
            if self.mode_id == 1: # Mode 1: Generate random data
                if sensor_type == "temperature":
                    data_temp["sensor_value"] = round(random.uniform(15, 30), 2)
                elif sensor_type == "battery_level":
                    data_temp["sensor_value"] = round(random.uniform(5, 80), 2)
                else:
                    data_temp["sensor_value"] = round(self.SB_IOT_GEN_DATA_ERROR_VALUE, 2)

            else: # Mode 2: Read data from JSON file
                file_name = os.path.join(self.root_path, "database", "iot_local_db" , f"{self.iot_device_id}.json")
                with open(file_name, "r") as json_file:
                    data_js = json.load(json_file)
                data_temp["sensor_value"] = round(data_js.get("sensors", {}).get(sensor_type, None), 2)
                
            data_temp["created_at"] = current_time
            data_temp["auto_mode"] = self.mode_id
            data_temp["synced_flag"] = 0
            
            iot_device.set_iot_data_struct(data_temp)
            return data.get_iot_data_struct()
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.log.logger.error(error_msg)
            return []
    
    def get_temperature(self):
        return self.__get_sensor_data("temperature")
    
    def get_battery_level(self):
        return self.__get_sensor_data("battery_level")
    
    