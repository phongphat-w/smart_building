import inspect
from datetime import datetime
import uuid

from django.db import models, migrations
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

import logging

# Set up a logger instance
logger = logging.getLogger("django")

class GuestManager(BaseUserManager):
    def create_user(self, first_name, last_name, password, email, checkin_date, checkout_date, building_id, floor_id, room_id, role_id):
        if not email:
            print(f"""{inspect.currentframe().f_code.co_name}(): Warning - The Email field must be set""")
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): The Email field must be set")
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)

        if checkin_date > checkout_date:
            print(f"""{inspect.currentframe().f_code.co_name}(): Warning - Kindly note - The check-in date cannot be later than the check-out date.""")
            logger.warning(f"{inspect.currentframe().f_code.co_name}(): Kindly note - The check-in date cannot be later than the check-out date.")
            raise ValueError("Kindly note - The check-in date cannot be later than the check-out date.")
        
        # # Check date format
        if isinstance(checkin_date, str):
            checkin_date = datetime.strptime(checkin_date, "%Y-%m-%dT%H:%M")  # Convert from string to datetime
        
        if isinstance(checkout_date, str):
            checkout_date = datetime.strptime(checkout_date, "%Y-%m-%dT%H:%M")  # Convert from string to datetime
        
        # Create a user instance
        user = self.model(first_name=first_name, last_name=last_name, email=email, checkin_date=checkin_date, checkout_date=checkout_date, building_id=building_id, floor_id=floor_id, room_id=room_id, role_id=role_id)
        
        # Hash and set password
        user.set_password(password)
        
        # Save the user object to the database
        user.save(using=self._db)
        return user

    # # Admin
    # def create_admin(self, first_name, last_name, password, email, building_id, role_id):
    #     user = self.create_user(first_name, last_name, password, email, building_id, role_id)        
    #     user.save(using=self._db)
    #     return user
    
    # # Staff
    # def create_staff(self, first_name, last_name, password, email, building_id, floor_id, role_id):
    #     user = self.create_user(first_name, last_name, password, email, building_id, floor_id, role_id)
    #     user.save(using=self._db)
    #     return user

class Guest(AbstractBaseUser):
    id = models.CharField(max_length=36, primary_key=True) # Django require field name, default: uuid_generate_v4(), config in DB directly.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    building_id = models.CharField(default="000",max_length=3)
    floor_id = models.CharField(default="0000", max_length=4)
    room_id = models.CharField(default="00000",max_length=5)
    is_active = models.BooleanField(default=True) #False, if require activation by email
    role_id = models.CharField(default=settings.SB_ROLE_ID.get("SB_ROLE_ID_GUEST") ,max_length=3) #table user_role.role_id: 003 is guest

    USERNAME_FIELD = "email"

    #The field named as the "USERNAME_FIELD" for a custom user model must not be included in "REQUIRED_FIELDS".
    # Password is required by default
    REQUIRED_FIELDS = ["first_name", "last_name", "checkin_date", "checkout_date", "building_id", "floor_id", "room_id", "role_id"] 

    objects = GuestManager() # Do not change variable name from "objects" to other, it is required by Django.

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    class Meta:
        app_label = "backend"


# Logging
class BackendLog(models.Model):
    id = models.CharField(max_length=36, primary_key=True) # Django require field name, default: uuid_generate_v4(), config in DB directly.
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=50)  # e.g., "DEBUG", "INFO", "ERROR", "CRITICAL"
    message = models.TextField()
    module = models.CharField(max_length=100, blank=True, null=True)  # Optional

    def __str__(self):
        return f"[{self.timestamp}] {self.level} - {self.message[:50]}"
    
    class Meta:
        # Specify the table name to match the hypertable
        db_table = "backend_log"