"""
This module contains ImagePostCreateService service class filling ImageModel object with data
provided in create form.
"""
from typing import Dict

from apps.image.models.image_model import ImageModel


class ImagePostCreateService:
    """
    Service class implementing mechanisms for filling an ImageModel object with data provided in
    ImagePostCreateForm class form.
    """

    def __init__(self, image_model: ImageModel, data: Dict):
        """
        Initializes class props.

        :param image_model: ImageModel object with uploaded image file and in DRAFT status
        :param data: ImagePostCreateForm form cleaned data dict
        """
        self._image_model = image_model
        self._data = data

    def execute(self, save=True):
        """
        Performs image_post attr fields filling and saves the object to database depending on
        save flag.

        :param save: saves to database when true
        """
        self.publish()
        self.add_location()
        self.add_datetime_taken()
        self.add_body()
        self.add_tags()
        if save:
            self._image_model.save()

    def publish(self):
        """Changes status to PUBLISHED."""
        self._image_model.status = ImageModel.PUBLISHED

    def add_location(self):
        """Adds an image taken place coordinates."""
        self._image_model.latitude = self._data['latitude']
        self._image_model.longitude = self._data['longitude']

    def add_body(self):
        """Adds post body."""
        self._image_model.body = self._data['body']

    def add_datetime_taken(self):
        """If not already stored adds datetime of an image taken."""
        if not self._image_model.datetime_taken:
            self._image_model.datetime_taken = self._data['datetime_taken']

    def add_tags(self):
        """Adds post tags"""
        self._image_model.tags.set(*self._data['tags'])
