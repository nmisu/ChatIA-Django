"""
Configuración completa de Django para el proyecto ChatIA.
"""
from pathlib import Path

# Definimos la ruta raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = "django-insecure-csr*_64eppac6=4jvqfv8@epa3b*2bcdvsvxrz=z1oy5brs1m4"
DEBUG = True

ALLOWED_HOSTS = [
    "django-chatia.onrender.com",
    "127.0.0.1",
    "localhost",
    '.pythonanywhere.com'
]

# Definición de aplicaciones
INSTALLED_APPS = [
    # Apps nativas de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Tus apps locales
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                'chat.context_processors.global_metrics', # <--- AÑADE ESTA LÍNEA EXACTA
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Base de datos
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Configuración de zona y lenguaje adaptada a la práctica
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = PROJECT_ROOT / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de redirecciones para el login/logout
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
