"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nnbjh58y3vj!i&8fddcl$2$39e+l63%qq0^$5yx2hi729+ynyr'

# SECURITY WARNING: don't run with debug turned on in production!



# Application definition

INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'django_celery_beat',
    'django_celery_results',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

# Media Files (Any file or image fields)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

UPLOAD_URL='/uploads'
UPLOAD_ROOT= os.path.join(BASE_DIR, 'uploads/')

# Increase maximum fields in order to allow for large admin actions
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

# Make debug depend on Env Var
DEBUG = os.environ.get('DEBUG','True').lower() == 'true'

# Allow all hosts (for better security set this to the real host name)
ALLOWED_HOSTS = ['*']

# Switch to arabic (change in case of english)
LANGUAGE_CODE = 'ar-eg'

# Use Egypt time zone
TIME_ZONE = 'Africa/Cairo'

# use dmy date format
USE_L10N = False
DATE_FORMAT = '%d-%m-%Y'


# Use postgres Database with a random db name when running tests
import string
import random


def random_choice():
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=8))



DATABASES = {
    'default': {

        'ENGINE': os.environ.get('SQL_ENGINE','django.db.backends.postgresql_psycopg2'),
        'NAME': os.environ.get('SQL_DB', 'internship2024'),
        'USER': os.environ.get('SQL_USER', 'admin'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', '1234'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),

    },
    'TEST':{'NAME': random_choice()}
}


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Allow iframes
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAdminUser',


    ],
      'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'dynamic_rest.renderers.DynamicBrowsableAPIRenderer',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Celery Settings
CELERY_RESULT_BACKEND = 'django-db'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL','amqp://guest:guest@localhost:5672//')



# Jazzmin Settings
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",

    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-nginxoutline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}



#jazzmin setting
JAZZMIN_SETTINGS = {
    "site_title": "Adhoc Admin",
    "site_header": "Adhoc",
    "site/static/_brand": "Adhoc",
    "site_logo": "jazzmin/img/logo.jpeg",
    "login_logo": "jazzmin/img/logo.jpeg",
    "login_logo_dark": "jazzmin/img/logo.jpeg",
    "site_logo_classes": "img-circle",
    "site_icon": "jazzmin/img/adhoc_logo.png",
    "welcome_sign": "Welcome to adhoc dashboard",
    "custom_css": "common/css/main.css",
    "custom_js" : "common/js/script.js",




    "topmenu_links": [

        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        {"model": "app.User"},

        {"app": "app"},
    ],
    "usermenu_links": [
        {"model": "app.User"}
    ],
    "show_sidebar": True,
    "navigation_expandednginx": True,

    "icons": {
        "auth": "fas fa-users-cog",
        "app.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "auth.Permission": "fas fa-shield-alt",
        "admin.LogEntry": "fas fa-file",
        "app.Employee": "fas fa-user",
        "app.Product": "fas fa-shopping-cart",
        "app.Project": "fab fa-product-hunt",
        "app.Country": "fas fa-globe",
        "app.Area": "fas fa-city",
        "app.Client": "fas fa-store",
        "app.Visit": "fas fa-stream",
        "app.Route": "fas fa-calendar",
        "app.Image": "fas fa-images",
        "app.DetectedImage": "fas fa-images",
        "app.Region": "fas fa-city",
        "app.City": "fas fa-globe",
        "app.Category": "fas fa-th",
        "app.Catalog": "fas fa-file-alt",
        "app.Tag": "fas fa-tags",
        "app.AreaTag": "fas fa-tags",
        "app.ClientTag": "fas fa-tags",
        "app.Audit": "fas fa-dolly-flatbed",
        "app.Day": "fas nginxfa-calendar-day",
        "app.Brand": "fas fa-th",
        "app.Channel": "fas fa-th",
        "app.Chain": "fas fa-sitemap",
        "app.SubCategory": "fas fa-sitemap",
        "app.Speciality": "fas fa-stream",
        "app.tab": "fas fa-stream",
        "app.Form": "fas fa-align-justify",
        "app.Answer": "fas fa-comment-dots",
        'app.Setting': 'fas fa-cogs',
        'app.Detection': 'fas fa-check-square',
        'app.Training': "fas fa-chart-bar",
        'app.ImageImport': "fas fa-file-archive",
        'app.DriveImport': "fas fa-download",
    },


    "hide_apps": [ 'authtoken'
                #   ,"django_celery_results"
                  ],
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        # "app.FormSubminginxssion": "horizontal_tabs",
        "auth.group": "vertical_tabs"},
    "order_with_respect_to": ["auth",'Users' ,"app", "app.User", 'app.Project','app.Region',  "app.Client",
                               'app.Route', 'app.Form','app.Question','app.Answer','app.SubCategory', "app.Product",
                              'app.Visit', 'app.Image','app.ImageImport', 'app.DriveImport','app.Setting'],
    "related_modal_active": False,


    "custom_links": {
    "auth": [{
        "name": "Users",
        "url": "/admin/app/user",
        "icon": "fas fa-user",
         }]
    },

    "hide_models": ['auth.Permission',
                    'app.User', 'app.Choice','app.ClientTag' , 'app.AreaTag', 'app.Brand',
                     'app.Chain', 'app.Channel', 'app.Country', 'app.Area', 'app.Catalog'
                    , 'app.Day', 'app.Speciality', 'app.Tab', 'app.Tag','app.City' ,
                    'app.Category', 'app.ImageType', 'app.SubTab','app.Detection',
                    'app.Question','app.QuestionGroup', 'app.FormSubmission', 'app.Status',
                    'app.ClientType', 'app.ParentTab', 'app.Audit',
                    'app.ImageLabel', 'app.AIModel',
                    'app.ImportTemplate'],




}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    # "sidebar_nav_legacy_style": True,

}


CSRF_TRUSTED_ORIGINS=[os.environ.get('DOMAIN','http://127.0.0.1')]