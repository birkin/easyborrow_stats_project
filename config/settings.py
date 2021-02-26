"""
#!/bin/bash

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json, logging, os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['EZB_STATS__SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads( os.environ['EZB_STATS__DEBUG_JSON'] )  # will be True or False

ADMINS = json.loads( os.environ['EZB_STATS__ADMINS_JSON'] )

ALLOWED_HOSTS = json.loads( os.environ['EZB_STATS__ALLOWED_HOSTS_JSON'] )  # list


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easyborrow_stats_app',
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

ROOT_URLCONF = 'config.urls'

template_dirs = json.loads( os.environ['EZB_STATS__TEMPLATES_JSON'] )
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': template_dirs,
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

## enabled by default, but disabled here as a reminder that django can be very lightweight

# db_path = os.path.join(f'{BASE_DIR}/../x_project_db/', 'x_project_db.sqlite3')
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         'NAME': db_path,
#     }
# }

DATABASES = json.loads( os.environ['EZB_STATS__DATABASES_JSON'] )


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


## Email
SERVER_EMAIL = 'easyborrow_stats@library.brown.edu'
EMAIL_HOST = os.environ['EZB_STATS__EMAIL_HOST']
print( f'EMAIL_HOST, ``{EMAIL_HOST}``' )
EMAIL_PORT = int( os.environ['EZB_STATS__EMAIL_PORT'] )
print( f'EMAIL_PORT, ``{EMAIL_PORT}``' )

## logging

## disable module loggers
# existing_logger_names = logging.getLogger().manager.loggerDict.keys()
# print '- EXISTING_LOGGER_NAMES, `%s`' % existing_logger_names
logging.getLogger('requests').setLevel( logging.WARNING )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': os.environ['EZB_STATS__LOG_PATH'],
            'formatter': 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'easyborrow_stats_app': {
            'handlers': ['logfile'],
            'level': os.environ['EZB_STATS__LOG_LEVEL'],
            'propagate': False
        },
        # 'django.db.backends': {  # re-enable to check sql-queries! <https://docs.djangoproject.com/en/1.11/topics/logging/#django-db-backends>
        #     'handlers': ['logfile'],
        #     'level': os.environ.get(u'BUL_CBP__LOG_LEVEL'),
        #     'propagate': False
        # },
    }
}
