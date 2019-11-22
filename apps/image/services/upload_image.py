from datetime import datetime
import os

from apps.image.services.image_processing.picture import Thumbnail
from apps.image.models.image_model import ImageModel
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


class UploadImage:

    def __init__(self, data):
        self._image = data['image']
        self._image_model = ImageModel()

    def create_draft(self):
        self._add_image()

        pic = Thumbnail.create_pic(self._image)

        self._add_thumbnail(pic)
        self._add_gps_coordinates(pic)
        self._add_image_taken_date_time(pic)
        self._image_model.save()
        return self._image_model

    def _add_gps_coordinates(self, pic):
        if not pic.exif_info:
            return None
        latitude, longitude = pic.exif_info.coordinates

        if latitude and longitude:
            self._image_model.latitude = latitude
            self._image_model.longitude = longitude

    def _add_thumbnail(self, pic):
        with pic.content_file as thumbnail:
            name, extension = os.path.splitext(self._image.name)
            thumbnail_name = '{}_thumb{}'.format(name, extension)
            self._image_model.thumbnail.save(thumbnail_name, thumbnail)

    def _add_image_taken_date_time(self, pic):
        if not pic.exif_info:
            return None
        date_time = pic.exif_info.date_time

        if date_time:
            date_time = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            date_time_list = parse_datetime(date_time)
            if not is_aware(date_time_list):
                date_time_list = make_aware(date_time_list)
            self._image_model.date_time_taken = date_time_list

    def _add_image(self):
        self._image_model.image = self._image
