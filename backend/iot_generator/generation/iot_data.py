# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import os
import sys
# Third-party library imports

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from backend.iot_generator.generation.iot_device_master import IotDevice # Absolute import
from backend.iot_generator.generation.iot_data_device_type import IotDataDeviceType # Absolute import

class IotData():
    def __init__(self, iot_device_id, mode_id):
        self.iot_device_id = iot_device_id
        self.mode_id = mode_id
        self.data = IotDataDeviceType(self.iot_device_id, self.mode_id)
    
    def get_data(self):
        if self.iot_device_id == IotDevice.get_device_id("thermostats"):
            return [self.data.get_temperature(), self.data.get_battery_level()]
        else:
            pass