"""
Django settings for RepoReaperGenerator project.
"""

from os import path
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ('localhost',)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(PROJECT_ROOT, 'db.sqlite3')
    }
}

TIME_ZONE = 'America/New_York'
USE_TZ = False
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = False
USE_THOUSAND_SEPARATOR = True
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = 'n(bd1f1c%e8=_xad02x5qtfn%wgwpi492e$8_erx+d)!tpeoim'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'DjangoWebProject.urls'

WSGI_APPLICATION = 'DjangoWebProject.wsgi.application'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'app',
)
