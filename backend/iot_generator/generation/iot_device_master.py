class IotDeviceMaster:
    iot_device = {}

    @classmethod
    def get_device_id(cls, device_key):
        cls.iot_device["thermostats"] = "7c84b98d-8f69-4959-ac5b-1b2743077151" #Smart thermostats

        return cls.iot_device[device_key]