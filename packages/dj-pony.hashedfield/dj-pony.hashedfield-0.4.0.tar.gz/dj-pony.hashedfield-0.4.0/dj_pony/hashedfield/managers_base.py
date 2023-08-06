import sentinel
from django.db import models
from dj_pony.hashedfield.fields import BinaryHashedField, EncodedHashedField


UseHashValue = sentinel.create("UseHashedValueInstead")


class PrecomputeHashesQuerysetMixin:
    """
    Override django queryset methods where we need to be able to pre-calculate hash values.

    This needs to come first in the class inheritance order to
    override some of the django methods that dont use super such as get_or_create.
    """
    def get_or_create(self: models.QuerySet, defaults=None, **kwargs):
        """
        Look up an object with the given kwargs, creating one if necessary.
        Return a tuple of (object, created), where created is a boolean
        specifying whether an object was created.
        """
        # The get() needs to be targeted at the write database in order
        # to avoid potential transaction consistency problems.
        self._for_write = True
        for _k, _v in kwargs.items():
            if _v is UseHashValue:
                for field in self.model._meta.get_fields():
                    if isinstance(field, (BinaryHashedField, EncodedHashedField)):
                        field_name = field.attname
                        if _k == field_name:
                            field.compute_hashed_value(self.model)
                            kwargs[_k] = field.value_from_object(self.model)
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            params = self._extract_model_params(defaults, **kwargs)
            return self._create_object_from_params(kwargs, params)

