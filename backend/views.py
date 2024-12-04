#User register, login, user's dashboard
from backend.views_utils.guest import register_guest, login_guest, refresh_token, get_user_devices

#Admin
from backend.views_utils.users import get_users

#Building's IOT devices
from backend.views_utils.devices import get_account_devices, get_building_devices, get_floor_devices, get_room_devices
