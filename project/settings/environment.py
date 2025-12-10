import os
from pathlib import Path
from utils.environment import get_env_variable, parse_comma_str_to_list



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p7t7f*uw$zfv=w#11j=@*@e7six80i60yexy7&vq0f3cikxlh@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = ALLOWED_HOSTS = parse_comma_str_to_list(get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS = parse_comma_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS'))
CSRS_ALLOWED_ORIGINS = parse_comma_str_to_list(get_env_variable('CORS_ALLOWED_ORIGINS'))


ROOT_URLCONF = 'project.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



WSGI_APPLICATION = 'project.wsgi.application'
