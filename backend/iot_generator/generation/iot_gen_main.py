# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import os
import sys
import time
from multiprocessing.pool import Pool

# Third-party library imports
from dotenv import load_dotenv

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Absolute import when run directly with python command
from backend.iot_generator.generation.iot_data import IotData 
from backend.iot_generator.generation.iot_config_file import IotConfigFile
from backend.iot_generator.generation.iot_store_local_db import IotStoreLocalDb
from backend.iot_generator.generation.iot_server_monitor import ServerHealthMonitor

class IotGenerator():
    def __init__(self, iot_device_id, mode_id):
        self.__load_config()

        self.iot_device_id = iot_device_id
        self.mode_id = mode_id

        # Initialize the server resource monitor         
        self.resource_monitor = ServerHealthMonitor(cpu_th=80, ram_th=80, disk_th=80, network_check=True)

        self.last_check_time = time.time()  # To track the time of the last resource check
        self.check_interval = 30  # Check every 30 seconds

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE")
        self.SB_GEN_DATA_MODE = os.getenv("SB_GEN_DATA_MODE")
        self.SB_GEN_DATA_FREQUENCY = int(os.getenv("SB_GEN_DATA_FREQUENCY"))
   
    def gen_iot_data(self):
        while True:
            current_time = time.time()
            # Check resources every self.check_interval seconds
            if current_time - self.last_check_time > self.check_interval:
                self.resource_monitor.wait_for_resources()
                self.last_check_time = current_time  # Update the time of the last check

            is_create, auto_mode = IotConfigFile(self.iot_device_id).create_iot_config_file()
            if is_create:
                data_list = IotData(self.iot_device_id, auto_mode).get_data() # Return as list
                if data_list: 
                    is_complete = IotStoreLocalDb(self.iot_device_id, data_list).store_data()
                    if is_complete:
                        print(f"""Data generated and stored successfully!", "iot_device_id": {self.iot_device_id}, "data_id": {data_list[-1]["data_id"]}""")
                    else:
                        print(f"""Data generated and stored fail!": {self.iot_device_id}, "data_id": {data_list[-1]["data_id"]}""")
                else:
                    print(f"""Cannot generate data", "iot_device_id": {self.iot_device_id}""")
            else:
                print(f"""Cannot create iot configure file", "iot_device_id": {self.iot_device_id}""")
            #
            time.sleep(self.SB_GEN_DATA_FREQUENCY)


def run_generator(iot_device_id):
    IotGenerator(iot_device_id).gen_iot_data()

#def gen_iot_data_main(): 
if __name__ == "__main__":

    iot_device_ids = [
        "7c84b98d-8f69-4959-ac5b-1b2743077151",  # Smart thermostats
        # "080d460f-e54c-4262-a4ac-a3d42c40cbd5",  # Demand-Controlled Ventilation (DCV)
        # "c0ec3c70-b76f-45e0-9297-8b5a4a462a47", #Smart bulbs and LED lights
        # "f531b9c1-c46a-42c4-989d-1d5be315f6a6", #Smart meters
        # "96b38698-d9ad-4355-807f-5580397471a1", #Presence sensors
        # "69b29098-c768-423e-ac2e-cc443e18f8a9", #Automated blinds or shades
    ]
    with Pool(processes=100) as pool:  # Limit concurrent processes
        pool.map(run_generator, iot_device_ids)

