# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import json
import os
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

from backend.iot_generator.generation.iot_device_struct import IotDeviceStruct # Absolute import
from backend.logging.system_logging import IotLogging # Absolute import

class IotConfigFile():
    def __init__(self, iot_device_id):
        self.__load_config()
        self.iot_device_id = iot_device_id
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 
        self.SB_PROJECT_STD_TIMEZONE = os.getenv("SB_PROJECT_STD_TIMEZONE") 
        self.SB_GEN_DATA_MODE = int(os.getenv("SB_GEN_DATA_MODE"))

    def create_iot_config_file(self):
        try:
            file_name = os.path.join(self.root_path, "database", "iot_local_db" , f"{self.iot_device_id}.json")
            if not os.path.exists(file_name):
                iot_config = IotDeviceStruct(self.iot_device_id).get_iot_device_struct()
                if iot_config:
                    # Write data to a JSON file
                    with open(file_name, "w") as json_file: 
                        json.dump(iot_config, json_file, indent=4)

                    print(f"""File "{self.iot_device_id}.json" created successfully.""")
                    return (True, 1)
                else:
                    return (False, 0)
        
            else:
                # print(f"""File "{file_name}" already exists.""")
                with open(file_name, "r") as json_file:
                    data = json.load(json_file)

                auto_flag = data.get("auto_flag", None)
                if auto_flag == 1:
                    print(f"""Auto generate mode is online...""")
                    return (True, 1)
                else:
                    print(f"""Auto generate mode is offline!""")
                    return (True, 0)
            
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.log.logger.error(error_msg)
            return (False, 0)
