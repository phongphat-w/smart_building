
# Python Enhancement Proposal 8 (PEP 8)

# Standard library imports
import inspect
import json
import os
import sys
import traceback
from datetime import datetime

# Third-party library imports
import pytz
from dotenv import load_dotenv

# Local application imports:
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print("DEBUG: project_root = " + project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from backend.database.db_connect import DbConnectServer # Absolute import
from backend.logging.system_logging import IotLogging # Absolute import

class IotInfo():
    def __init__(self, iot_device_id):
        self.__load_config()
        self.iot_device_id = iot_device_id
        self.log = IotLogging(self.SB_IOT_GET_INFO_LOG_FILE)

    def __load_config(self):
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        load_dotenv(dotenv_path=os.path.join(self.root_path, ".env"))

        self.SB_IOT_GET_INFO_LOG_FILE = os.getenv("SB_IOT_GET_INFO_LOG_FILE")
        self.SB_PROJECT_ACCOUNT_ID = os.getenv("SB_PROJECT_ACCOUNT_ID")
        self.SB_PROJECT_STD_TIMEZONE = os.getenv("SB_PROJECT_STD_TIMEZONE")
        self.SB_ROLE_ID_ADMIN = json.loads(os.getenv("SB_ROLE_ID")).get("SB_ROLE_ID_ADMIN")

    def get_iot_info(self):
        db = DbConnectServer()
        try:
            db.connect()
            query = f"""
                    SELECT a.account_id, c.client_id, c.client_name, d.country_name, d.time_zone
                    FROM iot_device a
                    INNER JOIN account b ON a.account_id = b.account_id
                    INNER JOIN client c ON b.client_id = c.client_id
                    INNER JOIN country d ON c.country_id = d.country_id
                    WHERE a.iot_device_id = %s
                    """
            params = (self.iot_device_id,)
            result = db.execute_read(query, params)            
            return result
        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            return None
        
        finally:
            db.close()

    def get_admin_info(self):
        db = DbConnectServer()
        try:
            db.connect()
            query = f"""
                    SELECT id, account_id, first_name, last_name, email, role_id, is_active, last_login 
                    FROM backend_user
                    WHERE account_id = %s AND role_id = %s
                    ORDER BY create_at
                    LIMIT 1
                    """
            params = (self.SB_PROJECT_ACCOUNT_ID, self.SB_ROLE_ID_ADMIN)
            result = db.execute_read(query, params)            
            return result

        except Exception as e:
            error_msg = f"""{datetime.now(pytz.timezone(self.SB_PROJECT_STD_TIMEZONE))}: {inspect.currentframe().f_code.co_name}(): Error - {e}\n{traceback.format_exc()}"""
            print(error_msg)
            self.logger.error(error_msg)
            return None
        
        finally:
            db.close()

    