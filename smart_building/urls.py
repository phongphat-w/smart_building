"""
URL configuration for smart_building project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path
from backend import views

# #favicon
# from django.views.static import serve
# from django.conf import settings
# from django.urls import re_path

#from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    #re_path(r'^favicon\.ico$', serve, {'path': 'favicon.ico', 'document_root': settings}),

    path("admin/", admin.site.urls),

    path("api/register_guest/", views.register_guest),
    path("api/login_guest/", views.login_guest),
    path("api/get_user_devices/", views.get_user_devices),

    # path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/refresh/', views.refresh_token),

    #Admin
    path("api/get_users/", views.get_users),

    path("api/adevices/<str:account_id>/",views.get_account_devices),
    path("api/bdevices/<str:account_id>/<str:building_id>/",views.get_building_devices),
    path("api/fdevices/<str:account_id>/<str:building_id>/<str:floor_id>/",views.get_floor_devices),
    path("api/rdevices/<str:account_id>/<str:building_id>/<str:floor_id>/<str:room_id>/",views.get_room_devices),
    
    #IOT Data
    path("api/device_data/<str:device_id>/",views.get_device_data),
    
]
