from django.conf import settings

try:
    AUTH_ANYFIELDS = settings.AUTH_ANYFIELDS
except AttributeError:
    AUTH_ANYFIELDS = ['username', 'email']

try:
    AUTH_ANYFIELDS_ONLY_UNIQUE_USERS = settings.AUTH_ANYFIELDS_ONLY_UNIQUE_USERS
except AttributeError:
    AUTH_ANYFIELDS_ONLY_UNIQUE_USERS = True

