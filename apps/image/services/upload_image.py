import os

from django.core.files.base import ContentFile

from apps.image.services.face_recognition.picture import Thumbnail
from apps.image.models.image_model import ImageModel


class UploadImage:

    def __init__(self, image):
        self._image = image

    def create_draft(self):
        image_model = self._factory_image_model()
        return image_model

    def _factory_image_model(self):
        image_model = ImageModel()

        with self._create_thumbnail() as thumbnail:
            name, extension = os.path.splitext(self._image.name)
            thumbnail_name = '{}_thumb{}'.format(name, extension)
            image_model.thumbnail.save(thumbnail_name, thumbnail)

        image_model.image = self._image
        image_model.save()

        return image_model

    def _create_thumbnail(self) -> ContentFile:
        return Thumbnail.create_pic(self._image).content_file
