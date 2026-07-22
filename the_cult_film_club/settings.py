from pathlib import Path
import os
import dj_database_url
from decimal import Decimal
from dotenv import load_dotenv

if os.path.isfile(".env"):
    load_dotenv()

SITE_ID = 1

# Debug mode (should be False in production)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Email is sent through Amazon SES, which has dominicfrancis.co.uk verified
# with DKIM, so any address on the domain can send.
#
# This replaced Fastmail SMTP, which rejected every message with
# "551 5.7.1 Not authorised to send from this header address" - the From
# address was not a configured sending identity on that account. Because the
# confirmation email was previously only sent on a path that almost never ran,
# the rejection went unnoticed.
#
# No credentials are configured: django-ses uses boto3, which picks up the
# EC2 instance role. The role may only send as the address below.
DEFAULT_FROM_EMAIL = "tcfc@dominicfrancis.co.uk"
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if not DEBUG:
    EMAIL_BACKEND = "django_ses.SESBackend"
    AWS_SES_REGION_NAME = "eu-west-2"
    AWS_SES_REGION_ENDPOINT = "email.eu-west-2.amazonaws.com"
    # django-ses throttles itself by calling ses:GetSendQuota before every
    # send. That action cannot be scoped to a resource, so allowing it would
    # mean granting it account-wide. This site sends a handful of messages a
    # day against a 14/second limit that SES enforces server-side regardless,
    # so the client-side throttle buys nothing worth widening IAM for.
    AWS_SES_AUTO_THROTTLE = None

# Custom user signup form for django-allauth
ACCOUNT_FORMS = {
    'login': 'the_cult_film_club.apps.account.forms.CustomLoginForm',
    'signup': 'the_cult_film_club.apps.account.forms.AccountSignupForm',
    'reset_password': (
        'the_cult_film_club.apps.account.forms.CustomResetPasswordForm'
    ),
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

# CSRF trusted origins for security. Read from the environment as a
# comma-separated list so the same code runs on Railway and on the AWS box;
# the default is the value that was previously hardcoded here, so leaving the
# variable unset keeps the existing deployment unchanged.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "http://127.0.0.1:8000/,https://*.herokuapp.com,"
        "https://*.railway.app,https://*.vercel.app",
    ).split(",") if o.strip()
]

# Allowed hosts for this Django site, same environment-driven approach.
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.railway.app,.vercel.app",
    ).split(",") if h.strip()
]

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
        },
        'image': {
            'toolbar': ['imageTextAlternative']
        }
    },
    'extends': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'underline', 'strikethrough',
            '|', 'bulletedList', 'numberedList', '|', 'outdent', 'indent',
            '|', 'link', 'blockQuote', '|', 'undo', 'redo'
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
        },
        'image': {
            'toolbar': ['imageTextAlternative']
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
# DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

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

# Django's default sends 500 tracebacks to ADMINS by email and prints nothing
# when DEBUG is False. With no ADMINS set, unhandled exceptions vanished
# silently. Writing to stderr instead puts them wherever the process log goes -
# the console in development, the systemd journal in production.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "the_cult_film_club": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
