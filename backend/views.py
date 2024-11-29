from django.http import JsonResponse
from django.shortcuts import render
from .database.db_connect import DbConnect
from django.contrib.auth import authenticate
import os
import inspect

#User register/login
from .views_utils.guest import register_guest, login_guest, get_user_devices

#Admin
from .views_utils.get_users import get_users

#Building
from .views_utils.building import get_building, get_floor, get_room
