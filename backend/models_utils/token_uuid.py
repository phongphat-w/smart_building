from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class UUIDToken(Token):
    # Overriding the user field to use UUID for the user reference
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, to_field="user_id", related_name="custom_tokens")
    
    class Meta:
        # Table name
        db_table = 'custom_auth_token'

