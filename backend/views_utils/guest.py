# import block according to alphabetical order and PEP 8 conventions style guide.

# Standard library imports
import os
import inspect
from datetime import datetime
import uuid
import logging

# Third-party imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

# Local application/library imports
from backend.models import Guest
from backend.models_utils.auth_backend import EmailBackend
from backend.serializers import GuestSerializer
from backend.database.db_connect import DbConnect

# Set up a logger instance
logger = logging.getLogger(__name__)

def create_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def register_guest(request):
    try:
        if request.method == "POST":
            # Extract data from the request
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
            if not first_name or not last_name or not password or not email or not checkin_date or not checkout_date or not building_id or not floor_id or not room_id:
                logger.warning(f"{inspect.currentframe().f_code.co_name}(): All fields are required, please verify.")
                return Response({"error": "All fields are required, please verify."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new guest
            guest = Guest.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                building_id=building_id,
                floor_id=floor_id,
                room_id=room_id
            )
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Guest created with user_id: {guest.id}")

            # Generate JWT tokens for the guest
            access_token, refresh_token = create_tokens_for_user(guest)
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Access Token: {access_token}")
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Refresh Token: {refresh_token}")

            # Serializer to return the guest data
            serializer = GuestSerializer(guest)

            # Return the guest data along with tokens
            return Response({
                "message": "Registration successful",
                "access_token": access_token,  # Access token
                "refresh_token": refresh_token,  # Refresh token
                "guest": serializer.data  # Return guest data
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"error": "Cannot register!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during registration: {e}")
        return Response({"error": f"Cannot register! - {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to login
def login_guest(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if email and password are provided
        if not email or not password:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): All fields are required, please verify.")
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user by using email as username
        email_backend = EmailBackend()
        user = email_backend.authenticate(request=request, username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user is active
        if not user.is_active:
            return Response({"error": "User is not active."}, status=status.HTTP_403_FORBIDDEN)

        # Generate access and refresh tokens for the user
        access_token, refresh_token = create_tokens_for_user(user)
        logger.info(f"{inspect.currentframe().f_code.co_name}(): Login successful for user: {user.id} with Access Token: {access_token}")

        # Return the tokens along with the user data
        return Response({
            "message": "Login successful",
            "access_token": access_token,  # Return access token, short-lived token
            "refresh_token": refresh_token,  # Return refresh token, long-lived token
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during login: {e}")
        return Response({"error": "Cannot login!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            logger.error(f"{inspect.currentframe().f_code.co_name}(): No refresh token provided")
            return Response({"error": "No refresh token provided"}, status=400)

        logger.info(f"{inspect.currentframe().f_code.co_name}(): Received refresh token: {refresh_token}")

        # Create RefreshToken object from the refresh token
        try:
            refresh = RefreshToken(refresh_token)
        except Exception as e:
            logger.error(f"{inspect.currentframe().f_code.co_name}(): Invalid refresh token: {e}")
            return Response({"error": "Invalid refresh token"}, status=400)

        # Issue a new access token
        access_token = str(refresh.access_token)
        logger.info(f"{inspect.currentframe().f_code.co_name}(): Generated access token: {access_token}")

        return Response({"access": access_token}, status=200)

    except Exception as e:
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during token refresh: {e}")
        return Response({"error": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_devices(request):
    root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), ".."))
    db = DbConnect(root_path=root_path)
    try:
        # Get the guest ID
        user_id = request.user.id
        logger.info(f"{inspect.currentframe().f_code.co_name}(): Fetching devices for user_id: {user_id}")

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
                    backend_guest b ON
                    a.building_id = b.building_id AND 
                    a.floor_id = b.floor_id AND 
                    a.room_id = b.room_id
                WHERE 
                    b.id = %s;
            """
        params = (user_id,)
        result = db.execute_query(sql_cmd, params)

        if result:
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Devices fetched successfully for user_id: {user_id}")
            return Response({"message": "Devices fetched successfully!", "user_id": user_id, "data": result}, status=status.HTTP_200_OK)
        else:
            logger.info(f"{inspect.currentframe().f_code.co_name}(): No device found for user_id: {user_id}")
            return Response({"message": "No device found for user.", "user_id": user_id, "data": result}, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error fetching devices: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        db.close()
