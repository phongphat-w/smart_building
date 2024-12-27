# Import block according to Python Enhancement Proposal 8 (PEP 8) guidelines.

# Standard library imports
from datetime import datetime
import inspect
import logging
import os

# Third-party imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Local application/library imports
from backend.database.db_connect import DbConnectServer

# Set up a logger instance
logger = logging.getLogger(__name__)

def gen_sql_thermostats():
    query_ = """
        (
        Select 1 as record_id, measured_at::date as measured_at_date, To_char(measured_at, 'yyyy-MM-dd HH:MI') as measured_at_time, sensor_type, sensor_value 
        From iot_data
        Where device_id = %s
        And sensor_type = %s
        And measured_at::date = NOW()::date
        Order by measured_at Desc
        Limit 1
        )
        Union All
        (Select 2 as record_id, measured_at::date as measured_at_date, To_char(measured_at, 'yyyy-MM-dd HH:MI') as measured_at_time, sensor_type, sensor_value 
        From iot_data
        Where device_id = %s
        And sensor_type = %s
        And measured_at::date = NOW()::date
        Order by measured_at Desc
        Limit 1
        )
        Order by record_id Asc
        """
    return query_

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_device_data(request):

    db = DbConnectServer()
    try:
        db.connect()
        device_id = request.device_id
        query = ""
        if device_id == "7c84b98d-8f69-4959-ac5b-1b2743077151": #Smart thermostats
            query = gen_sql_thermostats()
            params = (device_id, "temperature", device_id, "battery_level")
        else:
            pass

        result = db.execute_query(query, params)
        #if result != []:
        # print("result = ", result, "type of result = ", type(result))
        if result != "[]":    
            return Response({"message": "Retrieve data successfully!", "device_id": device_id, "data": result}, status=200)
        else:
            return Response({"message": "There is no data!", "device_id": device_id, "data": result}, status=200)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
        return Response({"message": "Get info fail!", "device_id": device_id}, status=400)
    
    finally:
        db.close()
