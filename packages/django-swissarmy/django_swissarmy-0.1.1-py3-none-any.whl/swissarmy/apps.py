from django.apps import AppConfig
from django.conf import settings

from .mixins.settings import set_default_setting
from . import defaults


class SwissarmyConfig(AppConfig):
    name = 'swissarmy'

    def ready(self):
        set_default_setting('UID_FIELD_SALT', defaults.UID_FIELD_SALT)
        set_default_setting('UID_HASH_MIN_LENGTH', defaults.UID_HASH_MIN_LENGTH)
        set_default_setting('UID_HASH_FORMAT', defaults.UID_HASH_FORMAT)
        set_default_setting('UID_HASH_ALPHABETS', defaults.UID_HASH_ALPHABETS)
        set_default_setting(
            'UID_HASH_ALPHABET',
            ''.join([
                settings.UID_HASH_ALPHABETS.get(x) for x in settings.UID_HASH_FORMAT
            ])
        )
