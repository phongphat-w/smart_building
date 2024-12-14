# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import multiprocessing

# Third-party imports

# Local application imports
from iot_gen_main import gen_iot_data_main
from iot_consume_main import consume_iot_data_main

process_gen_data = multiprocessing.Process(target=gen_iot_data_main)
process_consume_data = multiprocessing.Process(target=consume_iot_data_main)

process_gen_data.start()
process_consume_data.start()

process_gen_data.join()
process_consume_data.join()

print("Muti-generators and consumers are being executed parallelly...")
