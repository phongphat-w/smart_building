"""
Django settings for smart_building project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# from dotenv import load_dotenv
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["BASE_DIR"] = str(BASE_DIR)


#Django
SB__DJANGO_DEBUG = True
SB__DJANGO_DB_HOST = "localhost"
SB__DJANGO_DB_PORT = "5432"
SB__DJANGO_DB_NAME = "smart_building"
SB__DJANGO_DB_USER = "postgres"
SB__DJANGO_DB_PASSWORD = "password"

## Local DB
#SQLite
os.environ["SB__GEN_DATA_FREQUENCY"] = "5" #Second, must be string not integer

#IOT Json configuration file
os.environ["SB__GEN_DATA_MODE"] = "1" #Auto generate, must be string not integer

#TimeScaleDB
os.environ["SB__TIMESCALEDB_DB_HOST"] = "localhost"
os.environ["SB__TIMESCALEDB_DB_PORT"] = "5432"
os.environ["SB__TIMESCALEDB_DB_NAME"] = "smart_building"
os.environ["SB__TIMESCALEDB_DB_USER"] = "postgres"
os.environ["SB__TIMESCALEDB_DB_PASSWORD"] = "password"

os.environ["SB__USER_ADMIN_ID"] = "55a6d8ae-e242-45c1-8bd0-db4975cc366a"

#Kafka server
os.environ["SB__KAFKA_HOST"] = "localhost"
os.environ["SB__KAFKA_PORT"] = "9092"
os.environ["SB__KAFKA_DATA_FREQUENCY"] = "5" #Second, must be string not integer


#load_dotenv(dotenv_path = os.path.join(BASE_DIR, "configuration", ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y90jd^qnq+qr8rghsdw%$u84dt!kq0245r+@^sd0zngxwv(6c7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'backend',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    
    #'backend.apps.BackendConfig',  # Make sure the correct AppConfig is used
    
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',  # for browser interface
    ], 
    'TOKEN_MODEL': 'backend.models_utils.token_uuid.UUIDToken',  # Custom token model
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Adjust expiration time as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}
 
AUTHENTICATION_BACKENDS = (
    'backend.models_utils.auth_backend.EmailBackend',  # Modify this path based on file structure
    'django.contrib.auth.backends.ModelBackend',  # Fallback to default if needed
)

AUTH_USER_MODEL = 'backend.Guest' #app_label.ModelName

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # This must be at the top
    'django.middleware.common.CommonMiddleware', # Ensure this is below the CorsMiddleware

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # React frontend (127.0.0.1 for some cases)
]

#CORS_ALLOW_ALL_ORIGINS = True # Do not use in production

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',  # for Authorization headers / using tokens
    # Add other headers if needed
]

CORS_ALLOW_METHODS = [
    'GET', 'POST', 'OPTIONS',  # Adjust methods as needed
]

ROOT_URLCONF = 'smart_building.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'smart_building.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SB__TIMESCALEDB_DB_NAME"),
        "USER": os.getenv("SB__TIMESCALEDB_DB_USER"),
        "PASSWORD": os.getenv("SB__TIMESCALEDB_DB_PASSWORD"),
        "HOST": os.getenv("SB__TIMESCALEDB_DB_HOST"),
        "PORT": os.getenv("SB__TIMESCALEDB_DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#============================
# Logging system
#============================
"""
import os

# Ensure the logs directory exists
log_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set the logging level. Use 'DEBUG' for development and 'INFO' for production.
log_level = 'DEBUG'  # Captures all log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Timed Rotating File Handler for daily log rotation
        'timed_rotating_file': {
            'level': log_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'django.log'),
            'when': 'midnight',  # Rotate logs at midnight
            'interval': 1,  # Rotate every day
            'backupCount': 366,  # Retain logs for the last 366 days
            'formatter': 'verbose',
        },
        # Console Handler for real-time log output
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        # Verbose formatter for detailed logging output
        'verbose': {
            'format': '{asctime} - {levelname} - {module}: {message}',
            'style': '{',  # Use modern string formatting
        },
    },
    'loggers': {
        # Main Django logger
        'django': {
            'handlers': ['timed_rotating_file', 'console'],  # Log to file and console
            'level': log_level,  # Use the defined logging level
            'propagate': True,  # Allow propagation to parent loggers
        },
        # Database logger for SQL queries (if needed)
        'django.db.backends': {
            'handlers': ['timed_rotating_file'],  # Log SQL queries to file only
            'level': log_level,  # Use the defined logging level
            'propagate': False,  # Prevent logs from propagating to parent loggers
        },
    }
} # End Logging
"""
