"""
Django settings for config project.
"""
# 【ファイル責務】Django全体設定（DB・認証・静的配信・ストレージ）を管理
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティ設定
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# アプリケーション定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'knowledgeapp.apps.KnowledgeappConfig',
    # マイグレーションする時にaccountsアプリを参照してくれるようになる
    'accounts.apps.AccountsConfig',
]

USE_S3 = os.getenv('USE_S3', 'False') == 'True'
if USE_S3:
    # 【セクション】S3保存利用時のみstoragesアプリを有効化
    INSTALLED_APPS.append('storages')

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# データベース設定（MySQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'hackathon_db'),
        'USER': os.getenv('MYSQL_USER', 'dev_user'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 国際化設定
LANGUAGE_CODE = os.getenv('DJANGO_LANGUAGE_CODE', 'ja')
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'Asia/Tokyo')
USE_I18N = True
USE_TZ = True

# 静的ファイル
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# メディアファイル
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if USE_S3:
    # 【セクション】S3関連設定
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'ap-northeast-1')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', '')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

    media_location = os.getenv('AWS_MEDIA_LOCATION', 'uploads')
    storage_options = {
        'bucket_name': AWS_STORAGE_BUCKET_NAME,
        'region_name': AWS_S3_REGION_NAME,
        'file_overwrite': AWS_S3_FILE_OVERWRITE,
        'default_acl': AWS_DEFAULT_ACL,
        'querystring_auth': AWS_QUERYSTRING_AUTH,
        'location': media_location,
    }
    if AWS_S3_CUSTOM_DOMAIN:
        storage_options['custom_domain'] = AWS_S3_CUSTOM_DOMAIN

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': storage_options,
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }

    # default_storage.url() がS3 URLを返すように統一
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{media_location}/"
    else:
        MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{media_location}/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.User"

# LoginRequiredMixinを使うと、デフォルトでaccounts/login/というURLにリダイレクトされる
# accounts/login/以外にリダイレクトしたいなら、「LOGIN_URL =」 設定する必要がある
LOGIN_URL = "/login/"

# ログイン後にリダイレクトされるパスを設定
LOGIN_REDIRECT_URL = "/home/"

# ログアウト後にリダイレクトされるパスを設定
LOGOUT_REDIRECT_URL = '/login'
