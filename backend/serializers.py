from rest_framework import serializers
from .models import Guest
from django.contrib.auth import get_user_model
from .models import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["email", "first_name", "last_name", "password", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        guest = Guest.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data["password"],
            checkin_date = validated_data["checkin_date"],
            checkout_date = validated_data["checkout_date"],
            building_id = validated_data["building_id"],
            floor_id = validated_data["floor_id"],
            room_id = validated_data["room_id"],
        )
        return guest

#get all users
# #User = get_user_model()
# User = Guest()
# class GuestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "first_name", "last_name", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id", "is_active"]

