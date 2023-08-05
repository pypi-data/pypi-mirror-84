from django.conf import settings


def set_default_setting(key, default):
    if not hasattr(settings, key):
        setattr(settings, key, default)
