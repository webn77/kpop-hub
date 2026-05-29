"""
Django settings for KPOP HUB project.
"""

import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ───────────────────────────────────────────────
# Security — environment variable overrides
# ───────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# Render 운영 환경에서는 자동으로 DEBUG=False (로컬은 True 유지)
DEBUG = 'RENDER' not in os.environ
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
if DEBUG:
    # 개발 환경에서만 ngrok 터널 도메인 허용 (운영 공격면 축소)
    ALLOWED_HOSTS += ['.ngrok-free.app', '.ngrok-free.dev']
# Render가 주입하는 외부 호스트명 자동 허용
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ('localhost', '127.0.0.1')] + ['https://*.onrender.com']
if DEBUG:
    CSRF_TRUSTED_ORIGINS += ['https://*.ngrok-free.app', 'https://*.ngrok-free.dev']

# ───────────────────────────────────────────────
# 운영 환경 보안 헤더 (Render — DEBUG=False일 때만)
# ───────────────────────────────────────────────
if not DEBUG:
    # Render는 리버스 프록시 뒤에 있으므로 프록시 헤더로 HTTPS 인식 (리다이렉트 루프 방지)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1년
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ───────────────────────────────────────────────
# Application definition
# ───────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third-party
    'cloudinary',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_tailwind',
    'django_htmx',
    'mptt',
    # Local apps
    'accounts',
    'notices',
    'posts',
    'events',
    'polls',
    'surveys',
    'search',
    'admin_dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ───────────────────────────────────────────────
# Database — SQLite with WAL optimisation
# ───────────────────────────────────────────────
# DATABASE_URL 환경변수가 있으면 PostgreSQL(Render), 없으면 로컬 SQLite 사용
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,
                'init_command': (
                    'PRAGMA journal_mode=WAL; '
                    'PRAGMA synchronous=NORMAL; '
                    'PRAGMA foreign_keys=ON; '
                    'PRAGMA busy_timeout=20000;'
                ),
            },
        }
    }

# ───────────────────────────────────────────────
# Authentication
# ───────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_BY_CODE_ENABLED = False
# allauth 0.65+ 방식: 로그인 실패 5회 제한 (300초 잠금)
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/300s',
}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# ───────────────────────────────────────────────
# Password validation
# ───────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ───────────────────────────────────────────────
# Internationalization
# ───────────────────────────────────────────────
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# ───────────────────────────────────────────────
# Static & Media files
# ───────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 저장소: 로컬은 파일시스템 + 정적은 whitenoise.
# 운영(not DEBUG)은 업로드 미디어를 Cloudinary로 영구 저장 (Render 무료=휘발성 디스크 대응).
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
if not DEBUG:
    STORAGES['default']['BACKEND'] = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ───────────────────────────────────────────────
# Crispy Forms
# ───────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# ───────────────────────────────────────────────
# Default primary key field type
# ───────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
