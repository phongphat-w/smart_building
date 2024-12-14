# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import multiprocessing

# Third-party imports

# Local application imports
from iot_gen_blinds_shades import iot_generator as iot_generator_blinds_shades
from iot_gen_bulb_led import iot_generator as iot_generator_bulb_led
from iot_gen_dem_con_ven import iot_generator as iot_generator_dem_con_ven
from iot_gen_presence import iot_generator as iot_generator_presence
from iot_gen_smart_meter import iot_generator as iot_generator_smart_meter
from iot_gen_thermostats import iot_generator as iot_generator_thermostats

def run_thermostats():
    iot_device_id = "7c84b98d-8f69-4959-ac5b-1b2743077151"  # Smart thermostats
    iot_generator_thermostats(iot_device_id)

def run_dem_con_ven():
    iot_device_id = "080d460f-e54c-4262-a4ac-a3d42c40cbd5"  # Demand-Controlled Ventilation (DCV)
    iot_generator_dem_con_ven(iot_device_id)

def run_bulb_led():
    iot_device_id = "c0ec3c70-b76f-45e0-9297-8b5a4a462a47" #Smart bulbs and LED lights
    iot_generator_bulb_led(iot_device_id)

def run_smart_meter():
    iot_device_id = "f531b9c1-c46a-42c4-989d-1d5be315f6a6" #Smart meters
    iot_generator_smart_meter(iot_device_id)

def run_presence():
    iot_device_id = "96b38698-d9ad-4355-807f-5580397471a1" #Presence sensors
    iot_generator_presence(iot_device_id)

def run_blinds_shades():
    iot_device_id = "69b29098-c768-423e-ac2e-cc443e18f8a9" #Automated blinds or shades
    iot_generator_blinds_shades(iot_device_id)

def gen_iot_data_main():
    process_thermostats = multiprocessing.Process(target=run_thermostats)
    process_dem_con_ven = multiprocessing.Process(target=run_dem_con_ven)
    process_bulb_led = multiprocessing.Process(target=run_bulb_led)
    process_smart_meter = multiprocessing.Process(target=run_smart_meter)
    process_presence = multiprocessing.Process(target=run_presence)
    process_blinds_shades = multiprocessing.Process(target=run_blinds_shades)

    process_thermostats.start()
    process_dem_con_ven.start()
    process_bulb_led.start()
    process_smart_meter.start()
    process_presence.start()
    process_blinds_shades.start()

    process_thermostats.join()
    process_dem_con_ven.join()
    process_bulb_led.join()
    process_smart_meter.join()
    process_presence.join()
    process_blinds_shades.join()

    print("Muti-generators have completed execution.")
