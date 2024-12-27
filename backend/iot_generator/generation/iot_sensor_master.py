class IotSensorMaster:
    sensor_type = {}
    
    @classmethod
    def get_sensor_default(cls, sensor_key):
        cls.sensor_type["temperature"] = 25.00
        cls.sensor_type["battery_level"] = 100.00

        return cls.sensor_type[sensor_key]