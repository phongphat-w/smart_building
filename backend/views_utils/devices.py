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
# from ..models import IoTDevice
# from ..serializers import IoTDeviceSerializer

# Set up a logger instance
logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_account_devices(request, account_id):
    db = DbConnectServer()
    try:
        db.connect()
        query = """
            SELECT 
            a.iot_device_id
            , a. building_id
            , a. floor_id
            , a. room_id
            , a.device_sub_type_id
            , b.device_sub_type_name
            , b.device_type_id
            , c.device_type_name
            , a.account_id
            , d.account_name
            , d.client_id
            , e.client_name
            , e.country_id
            , f.country_name
            , f.time_zone
            , f.continent_id
            , g.continent_name
            FROM iot_device a 
            Inner Join device_sub_type b On a.device_sub_type_id = b.device_sub_type_id
            Inner Join device_type c On b.device_type_id = c.device_type_id
            Inner Join account d On a.account_id = d.account_id
            Inner Join client e On d.client_id = e.client_id
            Inner Join country f On e.country_id = f.country_id
            Inner Join continent g On f.continent_id = g.continent_id
            Where a.account_id = %s
            ORDER BY a.account_id, a.building_id, a.floor_id, a.room_id, b.device_type_id ASC 
        """
        params = (account_id,)
        result = db.execute_query(query, params)
        #if result != []:
        # print("result = ", result, "type of result = ", type(result))
        if result != "[]":    
            return Response({"message": "Retrieve data successfully!", "account_id": account_id, "data": result}, status=200)
        else:
            return Response({"message": "There is no data!", "account_id": account_id, "data": result}, status=200)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
        return Response({"message": "Get info fail!", "account_id": account_id}, status=400)
    
    finally:
        db.close()

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_building_devices(request, account_id, building_id):
    db = DbConnectServer()
    try:
        db.connect()
        query = """
            SELECT 
            a.iot_device_id
            , a. building_id
            , a. floor_id
            , a. room_id
            , a.device_sub_type_id
            , b.device_sub_type_name
            , b.device_type_id
            , c.device_type_name
            , a.account_id
            , d.account_name
            , d.client_id
            , e.client_name
            , e.country_id
            , f.country_name
            , f.time_zone
            , f.continent_id
            , g.continent_name
            FROM iot_device a 
            Inner Join device_sub_type b On a.device_sub_type_id = b.device_sub_type_id
            Inner Join device_type c On b.device_type_id = c.device_type_id
            Inner Join account d On a.account_id = d.account_id
            Inner Join client e On d.client_id = e.client_id
            Inner Join country f On e.country_id = f.country_id
            Inner Join continent g On f.continent_id = g.continent_id
            Where a.account_id = %s
            And a.building_id = %s
            ORDER BY a.account_id, a.building_id, a.floor_id, a.room_id, b.device_type_id ASC 
        """
        params = (account_id, building_id,)
        result = db.execute_query(query, params)
        #if result != []:
        # print("result = ", result, "type of result = ", type(result))
        if result != "[]":
            return Response({"message": "Retrieve data successfully!", "account_id": account_id, "building_id": building_id, "data": result}, status=200)
        else:
            return Response({"message": "There is no data!", "account_id": account_id, "building_id": building_id, "data": result}, status=200)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
        return Response({"message": "Get info fail!", "building_id": building_id}, status=400)
    
    finally:
        db.close()

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_floor_devices(request, account_id, building_id, floor_id):
    db = DbConnectServer()
    try:
        db.connect()
        query = """
            SELECT 
            a.iot_device_id
            , a. building_id
            , a. floor_id
            , a. room_id
            , a.device_sub_type_id
            , b.device_sub_type_name
            , b.device_type_id
            , c.device_type_name
            , a.account_id
            , d.account_name
            , d.client_id
            , e.client_name
            , e.country_id
            , f.country_name
            , f.time_zone
            , f.continent_id
            , g.continent_name
            FROM iot_device a 
            Inner Join device_sub_type b On a.device_sub_type_id = b.device_sub_type_id
            Inner Join device_type c On b.device_type_id = c.device_type_id
            Inner Join account d On a.account_id = d.account_id
            Inner Join client e On d.client_id = e.client_id
            Inner Join country f On e.country_id = f.country_id
            Inner Join continent g On f.continent_id = g.continent_id
            Where a.account_id = %s
            And a.building_id = %s
            And a.floor_id = %s
            ORDER BY a.account_id, a.building_id, a.floor_id, a.room_id, b.device_type_id ASC 
        """
        params = (account_id, building_id, floor_id)
        result = db.execute_query(query, params)
        #if result != []:
        # print("result = ", result, "type of result = ", type(result))
        if result != "[]":           
            return Response({"message": "Retrieve data successfully!", "account_id": account_id, "building_id": building_id, "floor_id": floor_id, "data": result}, status=200)
        else:
            return Response({"message": "There is no data!", "account_id": account_id, "building_id": building_id, "floor_id": floor_id, "data": result}, status=200)

    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
        return Response({"message": "Get info fail!", "building_id": building_id, "floor_id": floor_id}, status=400)
    
    finally:
        db.close()

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_room_devices(request, account_id, building_id, floor_id, room_id):
    db = DbConnectServer()
    try:
        db.connect()
        query = """
            SELECT 
            a.iot_device_id
            , a. building_id
            , a. floor_id
            , a. room_id
            , a.device_sub_type_id
            , b.device_sub_type_name
            , b.device_type_id
            , c.device_type_name
            , a.account_id
            , d.account_name
            , d.client_id
            , e.client_name
            , e.country_id
            , f.country_name
            , f.time_zone
            , f.continent_id
            , g.continent_name
            FROM iot_device a 
            Inner Join device_sub_type b On a.device_sub_type_id = b.device_sub_type_id
            Inner Join device_type c On b.device_type_id = c.device_type_id
            Inner Join account d On a.account_id = d.account_id
            Inner Join client e On d.client_id = e.client_id
            Inner Join country f On e.country_id = f.country_id
            Inner Join continent g On f.continent_id = g.continent_id          
            Where a.account_id = %s
            And a.building_id = %s
            And a.floor_id = %s
            And a.room_id = %s
            ORDER BY a.account_id, a.building_id, a.floor_id, a.room_id, b.device_type_id ASC 
        """
        params = (account_id, building_id, floor_id, room_id)
        result = db.execute_query(query, params)
        #if result != []:
        # print("result = ", result, "type of result = ", type(result))
        if result != "[]":           
            return Response({"message": "Retrieve data successfully!", "account_id": account_id, "building_id": building_id, "floor_id": floor_id, "room_id": room_id, "data": result}, status=200)
        else:
            return Response({"message": "There is no data!", "account_id": account_id, "building_id": building_id, "floor_id": floor_id, "room_id": room_id, "data": result}, status=200)

    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.error(f"{inspect.currentframe().f_code.co_name}(): {e}")
        return Response({"message": "Get info fail!", "building_id": building_id, "floor_id": floor_id, "room_id": room_id}, status=400)
    
    finally:
        db.close()

"""
@api_view(["POST"])
def control_device(request, device_id):
    try:
        device = IoTDevice.objects.get(id=device_id)
        temperature = request.data.get("temperature")

        if temperature is not None:
            device.temperature = temperature
            device.save()

        serializer = IoTDeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except IoTDevice.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
"""