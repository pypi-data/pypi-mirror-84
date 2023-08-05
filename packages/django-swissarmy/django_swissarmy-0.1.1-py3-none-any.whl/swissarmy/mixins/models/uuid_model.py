import uuid
from hashids import Hashids

from django.conf import settings
from django.db import models


class UidModelMixin(models.Model):
    """Unique ID type properties for a Django model.

    uuid is a concrete model field (i.e. it's stored in the DB) using uuid4.
    uid a concrete model field  based a (numerical) primary key using a hashid (https://hashids.org/).
    It uses the django SECRET_KEY as a salt to provide a degree of secrecy.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    uid = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.uid:
            self.uid = self.get_uid()
            super().save(update_fields=('uid',))

    def get_uid(self):
        """Unique id based on models pk.

        Returns:
            str: hashid if successful, otherwise string representation of pk (i.e. the model has a non-numerical PK)
        """
        try:
            uid = Hashids(
                salt=settings.UID_FIELD_SALT,
                min_length=settings.UID_HASH_MIN_LENGTH,
                alphabet=settings.UID_HASH_ALPHABET,
            ).encode(self.pk)
        except TypeError:
            uid = str(self.pk)
        return uid
