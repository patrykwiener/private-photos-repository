"""
This module contains Picture, Thumbnail and PictureForRecognition classes. Picture class
provides an abstraction for uploaded image file. Thumbnail represents a smaller version of the
uploaded image. PictureForRecognition creates shrunk image used for faster face recognition.
"""
from io import BytesIO
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile

from apps.image.services.image_processing.picture_exif_info import PictureExifInfo


class Picture:
    """
    This class provides an abstraction for uploaded image file. Its base class for Thumbnail
    and PictureForRecognition classes.
    """

    def __init__(self, image: Image, file_format: str, size: Tuple[int, int]):
        self._picture = image
        self._file_format = file_format
        self._exif_info = PictureExifInfo.create(image)
        self._original_size = image.size  # type: Tuple[int, int]
        self._picture.thumbnail(size, Image.ANTIALIAS)

    def rotate_when_turned(self) -> Image:
        """Rotates uploaded image depending on its orientation exif info value."""
        image = self._picture
        if self._exif_info:
            orientation = self._exif_info.orientation
            if orientation:
                try:
                    if orientation == 3:
                        image = self._picture.rotate(180, expand=True)
                    elif orientation == 6:
                        image = self._picture.rotate(270, expand=True)
                    elif orientation == 8:
                        image = self._picture.rotate(90, expand=True)
                except KeyError:
                    pass
        return image

    @staticmethod
    def convert_to_rgb(image: Image) -> Image:
        """Converts pil image colors to rgb."""
        rgb = 'RGB'
        if image.mode != rgb:
            return image.convert(rgb)
        return image

    @classmethod
    def create_pic(cls, image: ImageFieldFile, size=None) -> 'Picture':
        """
        Creates class instance.

        :param image: uploaded image
        :param size: size to shrink uploaded image
        :return: Picture class new instance
        """
        with image.open() as image:
            with Image.open(image) as image_opened:
                file_format = image_opened.format
                image_rgb = cls.convert_to_rgb(image_opened)
                instance = cls(image_rgb, file_format, size)
                instance._picture = instance.rotate_when_turned()
        return instance

    @property
    def exif_info(self) -> PictureExifInfo:
        """Returns image exif info."""
        return self._exif_info

    @property
    def file_format(self) -> str:
        """Returns image file format."""
        return self._file_format

    @property
    def original_size(self) -> Tuple[int, int]:
        """Returns image original dimensions."""
        return self._original_size

    @property
    def pic_size(self) -> Tuple[int]:
        """Returns current image dimensions."""
        return self._picture.size

    def close(self):
        """Closes pil image."""
        self._picture.close()


class Thumbnail(Picture):
    """Represents uploaded image thumbnail."""
    MAX_SIZE = (1200, 900)

    def __init__(self, image: Image, file_format: str, size=None):
        if size is None:
            size = self.max_size
        super().__init__(image, file_format, size)

    @property
    def max_size(self):
        """Returns thumbnail max size."""
        return self.MAX_SIZE

    @property
    def content_file(self) -> ContentFile:
        """Returns image byte representation required for creating new image file."""
        with BytesIO() as thumbnail_io:
            self._picture.save(thumbnail_io, format=self._file_format)
            content_file = ContentFile(thumbnail_io.getvalue())
        return content_file


class PictureForRecognition(Picture):
    """Represents shrunk version of uploaded image required for faster face recognition."""
    MAX_SIZE = (550, 550)

    def __init__(self, image: Image, file_format, size=None):
        if size is None:
            size = self.max_size
        super().__init__(image, file_format, size)

    @property
    def max_size(self):
        """Returns image for recognition max size."""
        return self.MAX_SIZE

    @property
    def pic_np(self):
        """Returns picture as numpy array"""
        return np.array(self._picture)

    @property
    def pic_np_gray_scale(self):
        """Returns picture in gray scale."""
        img_np = np.array(self._picture)
        return cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
