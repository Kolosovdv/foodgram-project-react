

import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6#00va*^87%lw60zz@9frf0m&x)a&_g76)wjpm0e(8!svrng3h'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['62.84.115.146', '127.0.0.1', 'localhost']
#ALLOWED_HOSTS = [*]


# Application definition

INSTALLED_APPS = [
    'logic.apps.LogicConfig',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'foodgram.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432')
        
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
AUTH_USER_MODEL = 'users.User'

DJOSER = {
        'LOGIN_FIELD': 'email',
        #'USER_ID_FIELD': 'id',
        #"SEND_ACTIVATION_EMAIL": False, #что бы при регистрации не отправлялась почта для подтверждение EMAIL
        #'HIDE_USERS': False, 

}


FOLLOW_YOURSELF_ERROR_MESSAGE = 'Нельзя подписаться на себя! =)'
FOLLOW_ERROR_MESSAGE = 'Вы уже подписаны на этого автора! =)'
EMAIL_ERROR_MESSAGE = 'Такой адрес электронной почты уже зарегистрирован! =)'
USERNAME_ERROR_MESSAGE = 'Такой логин уже зарегистрирован! =)'
IN_FAVORITE_MESSAGE = 'Этот рецепт уже в избранном! = )'
IN_SHOPPING_LIST_MESSAGE = 'Этот рецепт уже в вашем списке покупок! = )'
COOKING_TIME_MESSAGE = 'Время приготовления не может быть меньше 1-ой минуты!'
INGREDIENT_AMOUNT_MESSAGE = 'Ингредиента не может быть меньше 0!'
UNIQUE_INGREDIENT_MESSAGE = 'Ингредиенты не могут повторяться!'
ADD_TAG_MESSAGE = 'Добавь тег!'