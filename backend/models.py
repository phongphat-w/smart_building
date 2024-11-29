from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password

import datetime
import inspect
import uuid

class GuestManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, checkin_date, checkout_date, building_id, floor_id, room_id):
        if not email:
            print(f"""{inspect.currentframe().f_code.co_name}(): Warning - The Email field must be set""")
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        
        # Check date format
        if isinstance(checkin_date, str):
            checkin_date = datetime.datetime.strptime(checkin_date, "%Y-%m-%dT%H:%M")  # Convert from string to datetime
        
        if isinstance(checkout_date, str):
            checkout_date = datetime.datetime.strptime(checkout_date, "%Y-%m-%dT%H:%M")  # Convert from string to datetime
        
        # Create a user instance
        user = self.model(email=email, first_name=first_name, last_name=last_name, checkin_date=checkin_date, checkout_date=checkout_date, building_id=building_id, floor_id=floor_id, room_id=room_id)
        
        # Hash and set password
        user.set_password(password)
        
        # Save the user object to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Guest(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    building_id = models.CharField(default="000",max_length=3)
    floor_id = models.CharField(default="0000", max_length=4)
    room_id = models.CharField(default="00000",max_length=5)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = GuestManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id"]  # Password is required by default

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    class Meta:
        app_label = "backend"

       
#=====================================================



