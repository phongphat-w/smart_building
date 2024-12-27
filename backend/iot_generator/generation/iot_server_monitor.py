# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import os
import platform
import sys
import time
import traceback

# Third-party library imports
from dotenv import load_dotenv
import psutil

# Local application imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.logging.system_logging import IotLogging

class ServerHealthMonitor:
    def __init__(self, cpu_th=80, ram_th=80, disk_th=80, network_check=True):
        self.__load_config()
        self.cpu_th = cpu_th
        self.ram_th = ram_th
        self.disk_th = disk_th
        self.disk_io_th = 10_485_760 # 10 MB/s
        self.network_check = network_check
        self.log = IotLogging(self.SB_IOT_GEN_DATA_LOG_FILE)

        self.disk_type = self.get_disk_type()  # Get disk type (HDD/SSD)
        self.set_disk_io_threshold()  # Set the correct threshold based on disk type

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        # print("DEBUG: self.root_path = " + self.root_path)
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))
        self.SB_IOT_GEN_DATA_LOG_FILE = os.getenv("SB_IOT_GEN_DATA_LOG_FILE") 
        self.SB_IOT_GEN_DATA_PAUSE = os.getenv("SB_IOT_GEN_DATA_PAUSE")

    def get_disk_type(self):
        """
        Detect the disk type (HDD or SSD).
        """
        try:
            if platform.system().lower() == "windows":
                # On Windows, use psutil to check for HDD or SSD type
                for disk in psutil.disk_partitions():
                    if "Fixed" in disk.opts:  # Assuming "Fixed" is the type for physical drives
                        # Use `wmic` command to check disk type (HDD/SSD) on Windows
                        disk_info = os.popen(f"wmic diskdrive where index={disk.device.split(":")[1]} get MediaType").read()
                        if "SSD" in disk_info:
                            return "SSD"
                        else:
                            return "HDD"
            elif platform.system().lower() == "linux":
                # On Linux, check if the disk is SSD or HDD using `lsblk` command
                for disk in psutil.disk_partitions():
                    if disk.fstype:
                        # Run `lsblk` command to check the type of the disk
                        disk_info = os.popen(f"lsblk -d -o name,rota | grep {disk.device.split("/")[-1]}").read().split()
                        if disk_info and disk_info[1] == "0":
                            return "SSD"
                        else:
                            return "HDD"
            return "Unknown"
        except Exception as e:
            error_msg = f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"
            print(error_msg)
            self.log.logger.error(error_msg)
            return "Unknown"

    def set_disk_io_threshold(self):
        """
        Set the disk I/O thresholds based on the disk type (HDD or SSD).
        """
        if self.disk_type == "SSD":
            self.disk_io_th = 209_715_200  # 200 MB/s
        elif self.disk_type == "HDD":
            self.disk_io_th = 52_428_800  # 50 MB/s
        else:
            self.disk_io_th = 10_485_760  # 10 MB/s

    def check_resources(self):
        """
        Check the current system resource usage. If any resource exceeds the threshold, 
        return True indicating the system is under heavy load.
        """
        try:
            # Get current system resource usage
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage("/").percent  # Checking disk usage for the root directory
            disk_io = psutil.disk_io_counters()  # Checking the disk read/write speed
            network_info = psutil.net_if_stats()  # Checks network interface stats
            is_overload = False

            # Check CPU usage
            if cpu_usage > self.cpu_th:
                print(f"CPU usage {cpu_usage}% exceeds the threshold {self.cpu_th}%. Pausing process.")
                is_overload = True

            # Check RAM usage
            if ram_usage > self.ram_th:
                print(f"RAM usage {ram_usage}% exceeds the threshold {self.ram_th}%. Pausing process.")
                is_overload = True

            # Check disk usage
            if disk_usage > self.disk_th:
                print(f"Disk usage {disk_usage}% exceeds the threshold {self.disk_th}%. Pausing process.")
                is_overload = True

            # Check Disk I/O (read/write speed)
            if disk_io.read_bytes > self.disk_io_th or disk_io.write_bytes > self.disk_io_th:
                print(f"Disk I/O exceeds the threshold. Read bytes: {disk_io.read_bytes}, Write bytes: {disk_io.write_bytes}. Pausing process.")
                is_overload = True

            # Check network availability
            if self.network_check:
                active_network = False
                for interface, stats in network_info.items():
                    if stats.isup:  # If the network interface is up
                        active_network = True
                        break

                if not active_network:
                    print("No active network interfaces found. Pausing process.")
                    is_overload = True

            # Check server health (system crashes)
            if psutil.cpu_count() == 0:  # If no CPU is detected, the system might have crashed
                print("Server has no CPU available, likely crashed. Pausing process.")
                is_overload = True
            #
            return is_overload
        except Exception as e:
            error_msg = f"{inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"
            print(error_msg)
            self.log.logger.error(error_msg)
            return True # If cannot check; assume that is_overload = True

    def wait_for_resources(self):
        """
        Wait for the resources to fall below the threshold before resuming the process.
        """
        while self.check_resources(): #if overload
            print("Waiting for system resources to reduce below threshold...")
            time.sleep(int(self.SB_IOT_GEN_DATA_PAUSE))  # Wait for X seconds before checking again
        print("System resources are within limits. Resuming process.")
        print(f"{inspect.currentframe().f_code.co_name}(): System resources are within limits. Resuming process.")
