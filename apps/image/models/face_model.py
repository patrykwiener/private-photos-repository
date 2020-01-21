"""
This module contains FaceQuerySet class providing additional queries on FaceModel object set
and FaceModel class representing a person's face in an image.
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import QuerySet

from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class FaceQuerySet(QuerySet):
    """Represents additional lazy database lookups for FaceModel set of objects."""

    def encodings(self):
        """
        All face encodings getter.

        :return: all face encodings
        """
        return [instance.encoding for instance in self.all()]

    def people(self):
        """
        All people in an image getter.

        :return: all people on an image
        """
        return [instance.person for instance in self.all()]

    def recognized_faces(self):
        """
        All recognized faces getter.

        :return: all recognized faces
        """
        return self.exclude(person__isnull=True)


class FaceModel(models.Model):
    """Represents a person's face in an image."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_person = self.person

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

    objects = FaceQuerySet.as_manager()

    @property
    def original_person(self):
        """
        Originally assigned person getter.

        :return: originally assigned person
        """
        return self._original_person
