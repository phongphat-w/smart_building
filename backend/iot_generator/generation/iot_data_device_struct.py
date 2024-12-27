# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
from collections import defaultdict

# Third-party library imports

# Local application imports

class IotDataDeviceStruct:
    def __init__(self):
        # Initialize the data with default values
        self.__data = defaultdict(lambda: None, {
            "data_id": None,
            "device_id": None,
            "measured_at": None,
            "sensor_type": None,
            "sensor_value": None,
            "created_at": None,
            "auto_mode": None,
            "synced_flag": None
        })
    
    def get_iot_data_struct(self):
        """
        Returns the current state of the data structure.
        """
        return self.__data
    
    def set_iot_data_struct(self, data_dict):
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

    

                   