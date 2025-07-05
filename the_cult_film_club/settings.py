from pathlib import Path
import os
import dj_database_url
from decimal import Decimal

# Load environment variables from env.py if present (for local development)
if os.path.isfile("env.py"):
    import env  # noqa

# Debug mode (should be False in production)
DEBUG = False

# Email backend configuration for sending emails via Fastmail SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.fastmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
DEFAULT_FROM_EMAIL = "tcfc@dominicfrancis.co.uk"

# Custom user signup form for django-allauth
ACCOUNT_FORMS = {
    'signup': 'the_cult_film_club.apps.account.forms.AccountSignupForm',
}

# Allow login by email or username
ACCOUNT_LOGIN_METHODS = {"email", "username"}

# Fields required for signup (with * indicating required)
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "email2*",
    "username*",
    "password1*",
    "password2*",
]

# Require email verification for new accounts
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_MIN_LENGTH = 4

# Authentication URLs
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for Django (should be kept secret in production)
SECRET_KEY = os.environ.get("SECRET_KEY")

# CSRF trusted origins for security
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "https://*.herokuapp.com"]

# Allowed hosts for this Django site
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".herokuapp.com"]

# Installed apps (Django, third-party, and project apps)
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",  # For static files in development
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "cloudinary_storage",  # For media file storage
    "cloudinary",
    "whitenoise",  # For static file serving in production
    "the_cult_film_club.apps.home",
    "the_cult_film_club.apps.about",
    "the_cult_film_club.apps.account",
    "the_cult_film_club.apps.cart",
    "the_cult_film_club.apps.contact",
    "the_cult_film_club.apps.newsletter",
    "the_cult_film_club.apps.releases",
    "allauth",  # For authentication
    "allauth.account",
    "django_ckeditor_5",  # Rich text editor
    "crispy_forms",  # For improved form rendering
    "crispy_bootstrap5",  # Bootstrap 4 theme for crispy forms
]

# CKEditor 5 configuration for rich text editing
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', '|',
            'bulletedList', 'numberedList', '|', 'undo', 'redo'
        ],
        'heading': {
            'options': [
                {
                    'model': 'paragraph',
                    'title': 'Paragraph',
                    'class': 'ck-heading_paragraph'
                },
                {
                    'model': 'heading1',
                    'view': 'h1',
                    'title': 'Heading 1',
                    'class': 'ck-heading_heading1'
                },
                {
                    'model': 'heading2',
                    'view': 'h2',
                    'title': 'Heading 2',
                    'class': 'ck-heading_heading2'
                },
                {
                    'model': 'heading3',
                    'view': 'h3',
                    'title': 'Heading 3',
                    'class': 'ck-heading_heading3'
                },
            ]
        }
    }
}

# Use Bootstrap 5 for crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Middleware stack for request/response processing
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # For allauth
]

# Cloudinary storage configuration for media files
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    "SECURE": True,  # Use secure URLs for media files
}

# Static files storage configuration (using WhiteNoise)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default file storage for uploaded media
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Root URL configuration
ROOT_URLCONF = "the_cult_film_club.urls"

# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # required by allauth
                "django.template.context_processors.request",
                "the_cult_film_club.apps.cart.contexts.purchases",
            ],
            "builtins": [
                "crispy_forms.templatetags.crispy_forms_tags",
                "crispy_forms.templatetags.crispy_forms_field",
            ],
        },
    },
]

# Use session storage for Django messages
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Authentication backends (Django and allauth)
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Django admin login
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth login
]

# WSGI application entry point
WSGI_APPLICATION = "the_cult_film_club.wsgi.application"
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# This code commented out but kept for future automated testing
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Use database-backed sessions
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Database configuration (using dj_database_url for parsing DATABASE_URL)
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Localisation settings
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files (user uploads)
MEDIA_URL = "/assets/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom business logic settings
FREE_DELIVERY = 100
DELIVERY_RATE = Decimal('5')

# Stripe payment settings
FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10
STRIPE_CURRENCY = 'gbp'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')
