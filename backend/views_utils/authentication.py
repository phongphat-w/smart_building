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
from rest_framework.permissions import AllowAny

# Local application/library imports


# Set up a logger instance
logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_api_map(request):
    try:
        if request.method == "GET":
            # Return the guest data along with tokens
            config = settings.SB_MAP_TOKEN
            if config:
                return Response({
                    "message": "Get API key successful",
                    "data": config
                    }, status=status.HTTP_200_OK
                )
            else:
                logger.warning(f"{inspect.currentframe().f_code.co_name}(): Cannot get API key!")
                return Response({"warning": "Invalid API key!"}, status=status.HTTP_400_BAD_REQUEST)
        #    
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"warning": "Cannot get API key!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during get API Key: {e}")
        return Response({"error": f"Cannot get API key! - {e}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_gpt_con(request):
    try:
        if request.method == "GET":
            config_endpoint = settings.SB_GPT_AZURE_ENDPOINT
            config_apikey = settings.SB_GPT_API_KEY
            config_assistantid = settings.SB_GPT_ASSISTANT_ID

            if config_endpoint and config_apikey and config_assistantid:
                return Response({
                        "message": "Get Endpoint successful",
                        "data": {
                            "endpoint": settings.SB_GPT_AZURE_ENDPOINT,
                            "apikey": settings.SB_GPT_API_KEY,
                            "assistantid": settings.SB_GPT_ASSISTANT_ID
                        }
                    }, status=status.HTTP_200_OK
                )
            else:
                logger.warning(f"{inspect.currentframe().f_code.co_name}(): Cannot get GPT configuration!")
                return Response({"warning": "Invalid GPT configuration !"}, status=status.HTTP_400_BAD_REQUEST)
        #    
        else:
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Method is not accepted")
            return Response({"warning": "Cannot get GPT configuration!"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        logger.exception(f"{inspect.currentframe().f_code.co_name}(): Error during get GPT configuration: {e}")
        return Response({"error": f"Cannot get GPT configuration! - {e}"}, status=status.HTTP_400_BAD_REQUEST)