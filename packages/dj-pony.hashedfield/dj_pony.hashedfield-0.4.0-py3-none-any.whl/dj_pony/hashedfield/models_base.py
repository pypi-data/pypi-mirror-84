from django.db import models
from dj_pony.hashedfield.fields import BinaryHashedField, EncodedHashedField


class CalculateHashesMixin:
    """Mixin to help precalculate the hashed fields on a model for easier use with unique indexes."""
    def calculate_hashes(self: models.Model):
        for field in self._meta.fields:
            if isinstance(field, (BinaryHashedField, EncodedHashedField)):
                field.compute_hashed_value(self)


