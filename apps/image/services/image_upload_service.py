"""This module contains ImageUploadService service class uploading an image to the system."""
from datetime import datetime
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

from apps.image.services.image_processing.picture import Thumbnail, Picture
from apps.image.models.image_model import ImageModel

from apps.users.models import CustomUser


class ImageUploadService:
    """
    Service class creating ImageModel object and filling the object's attrs by including data
    read from image file.
    """

    def __init__(self, user: CustomUser, image: InMemoryUploadedFile):
        """
        Initializes class props.

        :param user: an uploading image file user
        :param image: uploaded image file
        """
        self._image = image
        self._image_model = ImageModel()
        self._image_model.user = user

    def upload(self):
        """Fills image_model attr with uploaded image file and data included within it."""
        self._add_image()

        pic = Thumbnail.create_pic(self._image_model.image)

        self._add_thumbnail(pic)
        self._add_gps_coordinates(pic)
        self._add_image_taken_date_time(pic)
        pic.close()

        self._image_model.save()
        return self._image_model

    def _add_gps_coordinates(self, pic: Picture):
        """
        Adds gps coordinates if they exist in image file.

        :param pic: Picture object containing uploaded image
        """
        if pic.exif_info:
            latitude, longitude = pic.exif_info.coordinates

            if latitude and longitude:
                self._image_model.latitude = latitude
                self._image_model.longitude = longitude

    def _add_thumbnail(self, pic: Thumbnail):
        """
        Adds thumbnail named by concatenating image file name and '_thumb'.

        :param pic: Thumbnail object
        """
        name, extension = os.path.splitext(self._image.name)
        thumbnail_name = '{}_thumb{}'.format(name, extension)
        self._image_model.thumbnail.save(thumbnail_name, pic.content_file)

    def _add_image_taken_date_time(self, pic: Picture):
        """
        If exists adds image taken datetime read from image file.

        :param pic: Picture object
        """
        if pic.exif_info:
            date_time = pic.exif_info.date_time

            if date_time:
                date_time = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S').strftime(
                    "%Y-%m-%d %H:%M:%S")
                date_time_list = parse_datetime(date_time)
                if not is_aware(date_time_list):
                    date_time_list = make_aware(date_time_list)
                self._image_model.datetime_taken = date_time_list

    def _add_image(self):
        """Adds uploaded image file."""
        self._image_model.image = self._image
        self._image_model.save()
