from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Handle OR conditions
#from django.contrib.auth import get_user_model
from backend.models import User
from rest_framework.pagination import PageNumberPagination
from backend.serializers import UserSerializer
import inspect

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


#User = get_user_model()
user = User()

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

@api_view(["GET"])
@permission_classes([AllowAny])  # Allow any user to register
def get_users(request):
    try:
        # Get the search query parameter, default to empty string if not provided
        search = request.GET.get("search", "")

        # If search query exists, filter users based on it
        if search:
           users = user.objects.filter(
                Q(first_name__icontains=search) | Q(email__icontains=search)
            )
        else:
            # If no search query, just get all users
            users = user.objects.all()

        # Ordered before pagination
        users = users.order_by("first_name")

        # Apply pagination
        paginator = UserPagination()
        result_page = paginator.paginate_queryset(users, request)

        # Serialize the result
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    except Exception as e:
        print(f"""{datetime.now()}: {inspect.currentframe().f_code.co_name}(): Error - {e}""")
        return Response({"error": "Cannot show users!"}, status=status.HTTP_400_BAD_REQUEST)

