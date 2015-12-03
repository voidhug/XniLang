#!/usr/bin/env python
#
#  Copyright 2015 XiaoJSoft Studio.
#
#  Use of this source code is governed by a proprietary license. You can not read, change or
#  redistribute this source code unless you have a written authorization from the copyright
#  holder listed above.
#

#  Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SERVER_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#  SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "2^pv^y&0w6ouqdj@qi#0-v_g)&xmi!m0!mix8x5=aklz26&9sz"

#  SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

#  Application definition.
INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
)
MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #  CSRF middleware is disabled by default.
    #  "django.middleware.csrf.CsrfViewMiddleware",
)
ROOT_URLCONF = "xnilang.urls"
WSGI_APPLICATION = "xnilang.wsgi.application"

#  Database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(SERVER_DIR, "internal", "db.sqlite3"),
    }
}

#  Internationalization.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

#  Static files (CSS, JavaScript, Images).
WEBAPP_BASE = "/app"
WEBAPP_DIR = os.path.join(SERVER_DIR, "static")
STATIC_URL = WEBAPP_BASE + "/"
STATICFILES_DIRS = (
    WEBAPP_DIR,
)
