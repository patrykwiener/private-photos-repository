from django.db import models
from django.utils.text import slugify


class RecognizedPersonModel(models.Model):
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)
