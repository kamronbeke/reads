from typing import Tuple

from django.db import models
from django.db.models import CharField


class Users(models.Model):
    name = models.CharField(max_length=100),
    email = models.TextField(),
    image = models.ImageField('goodreads/images'),
    first_name = models.CharField(max_length=150),

    def __str__(self):
        return self.email



