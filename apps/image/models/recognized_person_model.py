"""This module contains RecognizedPersonModel class representing recognized person personal data."""
from django.db import models
from django.utils.text import slugify


class RecognizedPersonModel(models.Model):
    """Represents recognized person personal data."""

    full_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        """Sets slug based on person's full name and saves an object to database."""
        if self.slug == "":
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)
