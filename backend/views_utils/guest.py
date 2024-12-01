from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.models import Guest 
from backend.models_utils.auth_backend import EmailBackend
from backend.serializers import GuestSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from backend.database.db_connect import DbConnect

from datetime import datetime
import os
import inspect
import uuid

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def register_guest(request):
    try:
        if request.method == "POST":
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            password = request.data.get("password")
            email = request.data.get("email")
            checkin_date = request.data.get("checkin_date")
            checkout_date = request.data.get("checkout_date")
            building_id = request.data.get("building_id")
            floor_id = request.data.get("floor_id")
            room_id = request.data.get("room_id")

            # Validate the input data
            if not email or not first_name or not last_name or not password or not checkin_date or not checkout_date:
                print(f"""{inspect.currentframe().f_code.co_name}(): Warning - All fields are required, please verify.""")
                return Response({"error": "All fields are required, please verify."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new guest
            guest = Guest.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                password = password,
                email = email,
                checkin_date = checkin_date,
                checkout_date = checkout_date,
                building_id = building_id,
                floor_id = floor_id,
                room_id = room_id
            )

            # Serializer to return the guest data
            serializer = GuestSerializer(guest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return Response({"Cannot register!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def login_guest(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        # Check required fields
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user by using email as username
        #user = authenticate(request, username=email, password=password)
        email_backend = EmailBackend()
        user = email_backend.authenticate(request=request, username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check active
        if not user.is_active:
            return Response({"error": "User is not active."}, status=status.HTTP_403_FORBIDDEN)

        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token to the user
        return Response({
            "message": "Login successful",
            "token": token.key  # Return the token key to the frontend
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return Response({"Cannot login!"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
#@permission_classes([AllowAny])  # Allow any user to register
def get_user_devices(request):
    root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    db = DbConnect(root_path=root_path)
    try:
        # Get the guest ID
        guest_id = request.user.id

        db.connect()
        sql_cmd = """
                SELECT 
                    a.iot_device_id, 
                    a.device_sub_type_id, 
                    a.account_id, 
                    a.building_id, 
                    a.floor_id, 
                    a.room_id
                FROM 
                    iot_device a
                JOIN 
                    backend_guest ON b
                    a.building_id = b.building_id AND 
                    a.floor_id = b.floor_id AND 
                    a.room_id = b.room_id
                WHERE 
                    b.id = %s;
            """
        params = (guest_id,)
        result = db.execute_query(sql_cmd, params)
        if result != []:    
            return Response({"message": "Retrieve data successfully!", "guest_id": guest_id, "result": result}, status=200)
        else:
            return Response({"message": "There is no data!", "guest_id": guest_id, "result": result}, status=200)
        
        db.close()
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"""{inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)