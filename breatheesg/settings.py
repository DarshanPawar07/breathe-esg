from pathlib import Path

import os


# ─────────────────────────────────────
# BASE DIR
# ─────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────
# SECURITY
# ─────────────────────────────────────

SECRET_KEY = (
    'django-insecure-breathe-esg'
)

DEBUG = True

ALLOWED_HOSTS = ['*']


# ─────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────

INSTALLED_APPS = [

    # Django
    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    # Third Party
    'rest_framework',

    'corsheaders',

    # Local Apps
    'core',
]


# ─────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─────────────────────────────────────
# URL CONFIG
# ─────────────────────────────────────

ROOT_URLCONF = 'breatheesg.urls'


# ─────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────

TEMPLATES = [

    {

        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

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


# ─────────────────────────────────────
# WSGI
# ─────────────────────────────────────

WSGI_APPLICATION = (
    'breatheesg.wsgi.application'
)


# ─────────────────────────────────────
# DATABASE
# ─────────────────────────────────────

DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.sqlite3',

        'NAME':
            BASE_DIR / 'db.sqlite3',
    }
}


# ─────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = []


# ─────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# ─────────────────────────────────────
# STATIC FILES
# ─────────────────────────────────────

STATIC_URL = 'static/'


# ─────────────────────────────────────
# MEDIA FILES
# ─────────────────────────────────────

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(
    BASE_DIR,
    'media'
)


# ─────────────────────────────────────
# UPLOAD DIRECTORIES
# ─────────────────────────────────────

UPLOAD_ROOT = os.path.join(
    BASE_DIR,
    'uploads'
)

SAP_UPLOAD_DIR = os.path.join(
    UPLOAD_ROOT,
    'sap'
)

UTILITY_UPLOAD_DIR = os.path.join(
    UPLOAD_ROOT,
    'utility'
)

TRAVEL_UPLOAD_DIR = os.path.join(
    UPLOAD_ROOT,
    'travel'
)


# Create upload folders automatically

os.makedirs(
    SAP_UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    UTILITY_UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    TRAVEL_UPLOAD_DIR,
    exist_ok=True
)


# ─────────────────────────────────────
# DEFAULT PRIMARY KEY
# ─────────────────────────────────────

DEFAULT_AUTO_FIELD = (
    'django.db.models.BigAutoField'
)


# ─────────────────────────────────────
# CORS
# ─────────────────────────────────────

CORS_ALLOW_ALL_ORIGINS = True


# ─────────────────────────────────────
# DJANGO REST FRAMEWORK
# ─────────────────────────────────────

REST_FRAMEWORK = {

    'DEFAULT_RENDERER_CLASSES': [

        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_PARSER_CLASSES': [

        'rest_framework.parsers.JSONParser',

        'rest_framework.parsers.MultiPartParser',

        'rest_framework.parsers.FormParser',
    ],
}