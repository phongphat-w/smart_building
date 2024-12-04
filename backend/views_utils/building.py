from rest_framework.response import Response
from django.shortcuts import render
from backend.database.db_connect import DbConnect
import os
import datetime
import inspect

root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", ".."))

def get_building(request, building_id):
    db = DbConnect(root_path=root_path)
    try:
        db.connect()
        sql_cmd = "Select * From iot_device Where building_id = %s "
        params = (building_id,)
        result = db.execute_query(sql_cmd, params)
        if result != []:    
            return Response({"message": "Retrieve data successfully!", "building_id": building_id, "result": result}, status=200)
        else:
            return Response({"message": "There is no data!", "building_id": building_id, "result": result}, status=200)
        
        db.close()
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        db.close()
        return Response({"message": "Get info fail!", "building_id": building_id}, status=400)


def get_floor(request, building_id, floor_id):
    db = DbConnect(root_path=root_path)
    try:
        db.connect()
        sql_cmd = "Select * From iot_device Where building_id = %s and floor_id = %s"
        params = (building_id, floor_id)
        result = db.execute_query(sql_cmd, params)
        if result != []:        
            return Response({"message": "Retrieve data successfully!", "building_id": building_id, "floor_id": floor_id, "result": result}, status=200)
        else:
            return Response({"message": "There is no data!", "building_id": building_id, "floor_id": floor_id, "result": result}, status=200)
        #
        db.close()
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        db.close()
        return Response({"message": "Get info fail!", "building_id": building_id, "floor_id": floor_id}, status=400)


def get_room(request, building_id, floor_id, room_id):
    db = DbConnect(root_path=root_path)
    try:
        db.connect()
        sql_cmd = "Select * From iot_device Where building_id = %s and floor_id = %s and room_id = %s"
        params = (building_id, floor_id, room_id)
        result = db.execute_query(sql_cmd, params)
        if result != []:        
            return Response({"message": "Retrieve data successfully!", "building_id": building_id, "floor_id": floor_id, "room_id": room_id, "result": result}, status=200)
        else:
            return Response({"message": "There is no data!", "building_id": building_id, "floor_id": floor_id, "room_id": room_id, "result": result}, status=200)
        #
        db.close()
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        db.close()
        return Response({"message": "Get info fail!", "building_id": building_id, "floor_id": floor_id, "room_id": room_id}, status=400)
