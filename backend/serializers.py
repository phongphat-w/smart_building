from .models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ["id", "first_name", "last_name", "password", "email", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id", "role_id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        guest = User.objects.create_user(  
            # id = validated_data["id"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data["password"],
            email = validated_data["email"],
            checkin_date = validated_data["checkin_date"],
            checkout_date = validated_data["checkout_date"],
            building_id = validated_data["building_id"],
            floor_id = validated_data["floor_id"],
            room_id = validated_data["room_id"],
            role_id = validated_data["role_id"],
        )
        return guest


#get all users
# #User = get_user_model()
# User = User()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "first_name", "last_name", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id", "is_active"]

