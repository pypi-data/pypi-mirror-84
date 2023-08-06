from django.db import models
from dj_pony.hashedfield.managers_base import PrecomputeHashesQuerysetMixin


class HashingQueryset(PrecomputeHashesQuerysetMixin, models.QuerySet):
    pass


class PreHashManager(models.Manager):
    def get_queryset(self):
        return HashingQueryset(model=self.model, using=self._db, hints=self._hints)


