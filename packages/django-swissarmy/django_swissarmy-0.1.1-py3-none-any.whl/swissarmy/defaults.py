from django.conf import settings

UID_FIELD_SALT = settings.SECRET_KEY
UID_HASH_MIN_LENGTH = 4
UID_HASH_FORMAT = ['lower', 'upper', 'number']
UID_HASH_ALPHABETS = {
    'lower': 'abcdefghijklmnopqrstuvwxyz',
    'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'number': '1234567890',
}
UID_HASH_ALPHABET = ''.join([
    UID_HASH_ALPHABETS.get(x) for x in UID_HASH_FORMAT
])
