import numpy as np
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import QuerySet
from django.utils.text import slugify

from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class FaceQuerySet(QuerySet):

    def encodings(self):
        return [instance.encoding for instance in self.all()]

    def people(self):
        return [instance.person for instance in self.all()]

    def recognized_faces(self):
        return self.exclude(person__isnull=True)


class FaceModel(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_person = self.person

    objects = FaceQuerySet.as_manager()

    @property
    def original_person(self):
        return self._original_person

    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    person = models.ForeignKey(
        RecognizedPersonModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    encoding = ArrayField(
        models.FloatField(),
        size=128
    )
    location = ArrayField(
        models.IntegerField(),
        size=4
    )
