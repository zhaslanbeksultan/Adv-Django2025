"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3hf$nybn$jnl=%i0nus9k_7ww0r-i2(6o-)k!*f$b+@dtgvl+c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'products.apps.ProductsConfig',
    'sales.apps.SalesConfig',
    'trading.apps.TradingConfig',
    'users.apps.UsersConfig',
    'cart.apps.CartConfig',
    'coupons.apps.CouponsConfig',
    'django_filters',
    'drf_yasg',
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

ROOT_URLCONF = 'mysite.urls'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',  # For Basic Auth
        # 'rest_framework.authentication.TokenAuthentication',   # For Token Auth
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # For JWT Auth
    )
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'users.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

CART_SESSION_ID = 'cart'
# Redirect after login
LOGIN_REDIRECT_URL = 'products'

# Redirect after logout
LOGOUT_REDIRECT_URL = 'login'

# Authentication backends (default)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

PDFKIT_OPTIONS = {
    'page-size': 'A4',
    'encoding': 'UTF-8',
}

# Set the path for wkhtmltopdf
PDFKIT_CONFIG = {
    'windows': r'E:\\wkhtmltox\\bin\\wkhtmltopdf.exe',  # For Windows
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Настроечные параметры Stripe
STRIPE_PUBLISHABLE_KEY = 'pk_test_51QvKFMJwx00zYYRSfPoMAf4cGecVKzyzwBq5TWJfSnjFL0qUxCU7Ovf0e2k9OBycbDRgQJtzeCMWkSgjEj09S2u200IgEcLsJ7' # Публикуемый ключ
STRIPE_SECRET_KEY = 'sk_test_51QvKFMJwx00zYYRS9MAHrN8zbQybflPvij9BAM1c1oCe5AoiI8QfRBbbgxm1htgfkO9ZcE5nbYhheTW7HLBosHGt00u3hxLWMq' # Секретный ключ
STRIPE_API_VERSION = '2022-08-01'
STRIPE_WEBHOOK_SECRET = 'whsec_8019a4d68b1607f37826c1df1e395952d73c6d989974d0d96ea7329036598c88'
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
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
STATIC_ROOT = BASE_DIR / 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
