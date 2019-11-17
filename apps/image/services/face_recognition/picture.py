from copy import deepcopy
from io import BytesIO
from typing import Tuple

import cv2
import numpy as np
from PIL import Image, ExifTags
from django.core.files.base import ContentFile


class Picture:

    def __init__(self, image: Image, file_format, size):
        self._picture = deepcopy(image)  # type: Image
        self._file_format = file_format
        self._picture.thumbnail(size, Image.ANTIALIAS)
        self._original_size = image.size  # type: Tuple[int]

    @staticmethod
    def rotate(image):

        orientation = list(ExifTags.TAGS.keys())[list(ExifTags.TAGS.values()).index('Orientation')]
        exif = image._getexif()
        if exif:
            try:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except KeyError:
                pass
        return image

    @classmethod
    def create_pic(cls, image, size=None):
        with Image.open(image) as image:
            file_format = image.format
            rgb = 'RGB'
            if image.mode != rgb:
                image = image.convert(rgb)
            image = cls.rotate(image)
            return cls(image, file_format, size)

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


class Thumbnail(Picture):
    MAX_SIZE = (1000, 1000)

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
    MAX_SIZE = (500, 500)

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
