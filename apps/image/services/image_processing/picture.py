from copy import deepcopy
from io import BytesIO
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile

from apps.image.services.image_processing.picture_exif_info import PictureExifInfo


class Picture:

    def __init__(self, image, file_format, size):
        self._picture = image  # type: Image
        self._file_format = file_format
        self._exif_info = PictureExifInfo.create(image)
        self._original_size = image.size  # type: Tuple[int]
        self._picture.thumbnail(size, Image.ANTIALIAS)

    def rotate_when_turned(self):
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
    def convert_to_rgb(image):
        rgb = 'RGB'
        if image.mode != rgb:
            return image.convert(rgb)
        return image

    @classmethod
    def create_pic(cls, image, size=None):
        with image.open() as image:
            with Image.open(image) as image_opened:
                file_format = image_opened.format
                image_rgb = cls.convert_to_rgb(image_opened)
                instance = cls(image_rgb, file_format, size)
                instance._picture = instance.rotate_when_turned()
        return instance

    @property
    def exif_info(self):
        return self._exif_info

    @property
    def file_format(self):
        return self._file_format

    @property
    def picture(self) -> Image:
        return self._picture

    @property
    def original_size(self) -> Tuple[int]:
        return self._original_size

    @property
    def pic_size(self) -> Tuple[int]:
        return self._picture.size

    def close(self):
        self._picture.close()


class Thumbnail(Picture):
    MAX_SIZE = (1200, 900)

    def __init__(self, image: Image, file_format, size=None):
        if size is None:
            size = self.max_size
        super().__init__(image, file_format, size)

    @property
    def max_size(self):
        return self.MAX_SIZE

    @property
    def content_file(self) -> ContentFile:
        with BytesIO() as thumbnail_io:
            self._picture.save(thumbnail_io, format=self._file_format)
            content_file = ContentFile(thumbnail_io.getvalue())
        return content_file


class PictureForRecognition(Picture):
    MAX_SIZE = (550, 550)

    def __init__(self, image: Image, file_format, size=None):
        if size is None:
            size = self.max_size
        super().__init__(image, file_format, size)

    @property
    def max_size(self):
        return self.MAX_SIZE

    @property
    def pic_np(self):
        return np.array(self._picture)

    @property
    def pic_np_gray_scale(self):
        img_np = np.array(self._picture)
        return cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
