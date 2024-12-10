# Import block according to Python Enhancement Proposal 8 (PEP 8) guidelines.

# Standard library imports
from datetime import datetime
import inspect
import logging

# Third-party imports
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

# Local application/library imports
from backend.database.db_connect import DbConnect
from backend.models import Guest
from backend.models_utils.auth_backend import EmailBackend
from backend.serializers import GuestSerializer

# Set up a logger instance
logger = logging.getLogger(__name__)

def create_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token

def get_user_info(email):
    db = DbConnect()
    try:
        if email == "":
            return "[]" #Json empty
        #
        db.connect()
        sql_cmd = """
                SELECT
                DISTINCT
                a.id
                , a.first_name
                , a.last_name
                , a.checkin_date::text
                , a.checkout_date::text
                , a.building_id
                , a.floor_id
                , a.room_id
                , a.is_active
                , a.is_admin
                , a.is_staff
                , a.last_login::text
                , b.account_id
                FROM backend_guest a
                INNER JOIN iot_device b on (a.building_id = b.building_id) AND (a.floor_id = b.floor_id) AND (a.room_id = b.room_id)
                WHERE a.email = %s;
            """
        params = (email,)
        result = db.execute_query(sql_cmd, params)

        if result:
            return result #Json
        else:
            return "[]" #Json empty
        
        db.close()
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error fetching user info: {e}")
        return "[]" #Json empty
        db.close()
       

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def register_guest(request):
    try:
        if request.method == "POST":
            data = request.data
            # Extract data from the request
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")
            email = data.get("email")
            checkin_date = data.get("checkin_date")
            checkout_date = data.get("checkout_date")
            building_id = data.get("building_id")
            floor_id = data.get("floor_id")
            room_id = data.get("room_id")

            # Validate the input data            
            required_fields = ["first_name", "last_name", "password", "email", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                logger.warning(f"Missing fields: {missing_fields}")
                return Response({"warning": f"All fields are required, please verify. Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new guest
            user = Guest.objGuestManager.create_user(
                #id: default
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                building_id=building_id,
                floor_id=floor_id,
                room_id=room_id,
                role_id=settings.SB_ROLE_ID.get("SB_ROLE_ID_GUEST")
            )
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Guest created with user_id: {user.id}")

            # Generate JWT tokens for the guest
            # access_token, refresh_token = create_tokens_for_user(guest)
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Access Token: {access_token}")
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Refresh Token: {refresh_token}")

            # Serializer to return the guest data
            serializer = GuestSerializer(user)

            # Return the guest data along with tokens
            return Response({
                "message": "Register successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"error": "Cannot register!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during registration: {e}")
        return Response({"error": f"Cannot register! - {e}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def register_staff(request):
    try:
        if request.method == "POST":
            data = request.data
            # Extract data from the request
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")
            email = data.get("email")
            building_id = data.get("building_id")
            floor_id = data.get("floor_id")
            role_id = data.get("role_id")

            # Validate the input data            
            required_fields = ["first_name", "last_name", "password", "email", "building_id", "floor_id", "role_id"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                logger.warning(f"Missing fields: {missing_fields}")
                return Response({"warning": f"All fields are required, please verify. Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new guest
            user = Guest.objGuestManager.create_staff(
                #id: default
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                building_id=building_id,
                floor_id=floor_id,
                role_id=settings.SB_ROLE_ID.get("SB_ROLE_ID_STAFF")
            )
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Guest created with user_id: {user.id}")

            # Generate JWT tokens for the guest
            # access_token, refresh_token = create_tokens_for_user(guest)
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Access Token: {access_token}")
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Refresh Token: {refresh_token}")

            # Serializer to return the guest data
            serializer = GuestSerializer(user)

            # Return the guest data along with tokens
            return Response({
                "message": "Register successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"error": "Cannot register!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during registration: {e}")
        return Response({"error": f"Cannot register! - {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([AllowAny])  # Allow any user to register
def register_admin(request):
    try:
        if request.method == "POST":
            data = request.data
            # Extract data from the request
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")
            email = data.get("email")
            building_id = data.get("building_id")
            # floor_id = data.get("floor_id")
            role_id = data.get("role_id")

            # Validate the input data            
            required_fields = ["first_name", "last_name", "password", "email", "building_id", "role_id"]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                logger.warning(f"Missing fields: {missing_fields}")
                return Response({"warning": f"All fields are required, please verify. Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new guest
            user = Guest.objGuestManager.create_admin(
                #id: default
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                building_id=building_id,
                # floor_id=floor_id,
                role_id=settings.SB_ROLE_ID.get("SB_ROLE_ID_ADMIN")
            )
            logger.info(f"{inspect.currentframe().f_code.co_name}(): Guest created with user_id: {user.id}")

            # Generate JWT tokens for the guest
            # access_token, refresh_token = create_tokens_for_user(guest)
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Access Token: {access_token}")
            # logger.info(f"{inspect.currentframe().f_code.co_name}(): Refresh Token: {refresh_token}")

            # Serializer to return the guest data
            serializer = GuestSerializer(user)

            # Return the guest data along with tokens
            return Response({
                "message": "Register successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"error": "Cannot register!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
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
        
        user_info = get_user_info(email)
        if user_info == "[]":
            return Response({"error": "Cannot get user information"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("DEBUG: user_info = ", user_info)
            return Response({
                "message": "Login successful",
                "data": {
                    "sb_access_token": access_token,  # Return access token, short-lived token
                    "sb_refresh_token": refresh_token,  # Return refresh token, long-lived token
                    "sb_user_info": user_info, # User info
                }
            }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
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
            print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
            logger.error(f"{inspect.currentframe().f_code.co_name}(): Invalid refresh token: {e}")
            return Response({"error": "Invalid refresh token"}, status=400)

        # Issue a new access token
        access_token = str(refresh.access_token)
        logger.info(f"{inspect.currentframe().f_code.co_name}(): Generated access token: {access_token}")

        return Response({"access": access_token}, status=200)

    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during token refresh: {e}")
        return Response({"error": str(e)}, status=400)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_user_devices(request):
#     db = DbConnect()
#     try:
#         # Get the guest ID
#         user_id = request.user.id
#         logger.info(f"{inspect.currentframe().f_code.co_name}(): Fetching devices for user_id: {user_id}")

#         db.connect()
#         sql_cmd = """
#                 SELECT 
#                     a.iot_device_id, 
#                     a.device_sub_type_id, 
#                     a.account_id, 
#                     a.building_id, 
#                     a.floor_id, 
#                     a.room_id
#                 FROM 
#                     iot_device a
#                 JOIN 
#                     backend_guest b ON
#                     a.building_id = b.building_id AND 
#                     a.floor_id = b.floor_id AND 
#                     a.room_id = b.room_id
#                 WHERE 
#                     b.id = %s;
#             """
#         params = (user_id,)
#         result = db.execute_query(sql_cmd, params)

#         if result:
#             logger.info(f"{inspect.currentframe().f_code.co_name}(): Devices fetched successfully for user_id: {user_id}")
#             return Response({"message": "Devices fetched successfully!", "user_id": user_id, "data": result}, status=status.HTTP_200_OK)
#         else:
#             logger.info(f"{inspect.currentframe().f_code.co_name}(): No device found for user_id: {user_id}")
#             return Response({"message": "No device found for user.", "user_id": user_id, "data": result}, status=status.HTTP_200_OK)
    
#     except Exception as e:
#         print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
#         logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error fetching devices: {e}")
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     finally:
#         db.close()

