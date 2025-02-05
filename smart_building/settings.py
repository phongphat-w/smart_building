"""
Django settings for smart_building project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from dotenv import load_dotenv
import json
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["BASE_DIR"] = str(BASE_DIR)

#=========================================================
# Load environment variables from .env file
#=========================================================
load_dotenv(dotenv_path = os.path.join(BASE_DIR, "backend" , ".env"))


# Back-end (Django) -------------------------------------

SB_PROJECT_NAME=os.getenv("SB_PROJECT_NAME")
SB_PROJECT_ACCOUNT_ID=os.getenv("SB_PROJECT_ACCOUNT_ID")

#Django
SB_DJANGO_SECRET_KEY=os.getenv("SB_DJANGO_SECRET_KEY")
SB_DJANGO_DEBUG=os.getenv("SB_DJANGO_DEBUG")

SB_DJANGO_DB_HOST=os.getenv("SB_DJANGO_DB_HOST")
SB_DJANGO_DB_PORT=os.getenv("SB_DJANGO_DB_PORT")
SB_DJANGO_DB_NAME=os.getenv("SB_DJANGO_DB_NAME")
SB_DJANGO_DB_USER=os.getenv("SB_DJANGO_DB_USER")
SB_DJANGO_DB_PASSWORD=os.getenv("SB_DJANGO_DB_PASSWORD")

# Access specific roles
try:
    SB_ROLE_ID = json.loads(os.getenv("SB_ROLE_ID", "{}"))
except json.JSONDecodeError:
    raise ValueError("Invalid SB_ROLE_ID format in .env file")

## Local DB
#SQLite
SB_GEN_DATA_FREQUENCY=os.getenv("SB_GEN_DATA_FREQUENCY")

#IOT Json configuration file
SB_IOT_GEN_DATA_MODE=os.getenv("SB_IOT_GEN_DATA_MODE")

#TimeScaleDB
SB_TIMESCALEDB_DB_HOST=os.getenv("SB_TIMESCALEDB_DB_HOST")
SB_TIMESCALEDB_DB_PORT=os.getenv("SB_TIMESCALEDB_DB_PORT")
SB_TIMESCALEDB_DB_NAME=os.getenv("SB_TIMESCALEDB_DB_NAME")
SB_TIMESCALEDB_DB_USER=os.getenv("SB_TIMESCALEDB_DB_USER")
SB_TIMESCALEDB_DB_PASSWORD=os.getenv("SB_TIMESCALEDB_DB_PASSWORD")

#Kafka server
SB_KAFKA_HOST=os.getenv("SB_KAFKA_HOST")
SB_KAFKA_PORT=os.getenv("SB_KAFKA_PORT")
SB_KAFKA_DATA_FREQUENCY=os.getenv("SB_KAFKA_DATA_FREQUENCY")


# Front-end (React.js) -------------------------------------

SB_MAP_TOKEN = os.getenv("SB_MAP_TOKEN")
SB_GPT_AZURE_ENDPOINT = os.getenv("SB_GPT_AZURE_ENDPOINT")
SB_GPT_API_KEY = os.getenv("SB_GPT_API_KEY")
SB_GPT_ASSISTANT_ID = os.getenv("SB_GPT_ASSISTANT_ID")

#=========================================================

#SSL https
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True



# Define Kafka Consumer configuration
consumer_config = {
    "bootstrap.servers": f"""{os.getenv("SB_KAFKA_HOST")}:{os.getenv("SB_KAFKA_PORT")}""",  # Kafka server
    "group.id": "iot-consumer-group",
    "auto.offset.reset": "earliest"  # Start from the earliest message
}



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SB_DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'backend',] #'backend': docker url used by Prometheus


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
    'channels',
	
	'django_extensions',
    'django_prometheus',
    
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

AUTH_USER_MODEL = 'backend.User' #app_label.ModelName

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ASGI_APPLICATION = 'smart_building.asgi.application'

# Redis Channel Layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],  # Use the Redis container name
        },
    },
}

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',


    'corsheaders.middleware.CorsMiddleware', # This must be at the top
    'django.middleware.common.CommonMiddleware', # Ensure this is below the CorsMiddleware

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    

     'django_prometheus.middleware.PrometheusAfterMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # React frontend (127.0.0.1 for some cases)
	"https://localhost:3000",  # React frontend SSL
    "https://127.0.0.1:3000",  # React frontend (127.0.0.1 for some cases) SSL
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
        "HOST": SB_DJANGO_DB_HOST,
        "PORT": SB_DJANGO_DB_PORT,
        "NAME": SB_DJANGO_DB_NAME,
        "USER": SB_DJANGO_DB_USER,
        "PASSWORD": SB_DJANGO_DB_PASSWORD,
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

LANGUAGE_CODE = 'en-us'  # Can keep this as 'en-us' or change to 'th' for Thai

USE_TZ = True  # Enable timezone support
TIME_ZONE = 'UTC'  # Convert to local when display

USE_I18N = True  # Internationalization (Translation support)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#============================
# Logging system
#============================

# Ensure the logs directory exists
log_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set the logging level. Use 'DEBUG' for development and 'INFO' for production.
DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL")  # DEBUG captures all log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
DJANGO_LOG_BACKUP_COUNT = os.getenv("DJANGO_LOG_BACKUP_COUNT") # Days to keep log

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Timed Rotating File Handler for daily log rotation
        'timed_rotating_file': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'django.log'),
            'when': 'midnight',  # Rotate logs at midnight
            'interval': 1,  # Rotate every day
            'backupCount': DJANGO_LOG_BACKUP_COUNT,  # Retain logs for the last 500 days
            'formatter': 'verbose',
        },
        # Console Handler for real-time log output
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # DB log
        'db': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'backend.models_utils.log_handler.DatabaseLogHandler',  # Path to DatabaseLogHandler()
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
        # Main Django logger (Parent Log)
        'django': {
            'handlers': [
                        'timed_rotating_file', 
                        #  'db', 
                        #  'console'
                         ],  # Log to file, database and console
            'level': DJANGO_LOG_LEVEL,  # Use the defined logging level
            'propagate': True,  # Allow propagation to parent loggers
        },
        # Database logger for SQL queries (Child Log)
        'django.db.backends': {
            'handlers': [
                        'timed_rotating_file', 
                        #  'db', 
                        #  'console'
                         ],  # Log to file, database and console
            'level': DJANGO_LOG_LEVEL,  # Use the defined logging level
            'propagate': False,  # Prevent logs from propagating to parent loggers (Main Django logger)
        },
    }
} # End Logging
