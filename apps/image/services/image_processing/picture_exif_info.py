"""This module contains PictureExifInfo class providing jpeg image exif metadata access."""
from typing import Dict, Tuple, Optional

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class PictureExifInfo:
    """Provides access to jpeg image exif metadata."""

    def __init__(self, exif: Dict):
        """
        Initializes exif property with decoded exif info dict.

        :param exif: dict containing image exif info
        """
        self._exif = self._get_labeled_exif(exif)

    @staticmethod
    def _get_labeled_exif(exif: Dict) -> Dict:
        """
        Converts exif dict keys from numerical to correctly labeled ones.

        :param exif: image exif dict
        :return: decoded exif info
        """
        for key, _ in exif.items():
            exif[TAGS.get(key, key)] = exif.pop(key)
        return exif

    @staticmethod
    def _get_decimal_coordinate(dimension, reference):

        degrees = dimension[0][0] / dimension[0][1]
        minutes = dimension[1][0] / dimension[1][1] / 60
        seconds = dimension[2][0] / dimension[2][1] / 3600

        if reference in ['W', 'S']:
            degrees = - degrees
            minutes = - minutes
            seconds = - seconds

        return degrees + minutes + seconds

    @classmethod
    def create(cls, pil_image: Image) -> Optional['PictureExifInfo']:
        """
        Creates PictureExifInfo object by call its constructor when the pil_image contains exif
        metadata.

        :param pil_image: PIL image
        :return: PictureExifInfo instance or None when pil_image does not contain exif info
        """
        exif = getattr(pil_image, '_getexif', lambda: None)()
        if exif:
            return cls(exif)

    @property
    def geo_tags(self) -> Optional[Dict]:
        """
        Returns dict of GPSInfo exif info with labeled keys.
        """
        gps_info_tag = 'GPSInfo'
        if gps_info_tag in self._exif:
            gps_tags = {}
            for gps_key, gps_tag in GPSTAGS.items():
                if gps_key in self._exif[gps_info_tag]:
                    gps_tags[gps_tag] = self._exif[gps_info_tag][gps_key]

            return gps_tags

    @property
    def coordinates(self) -> Tuple[Optional[float], Optional[float]]:
        """
        Returns tuple containing decimal gps coordinates read from image exif info.
        """
        geo_tags = self.geo_tags
        latitude, longitude = None, None
        if geo_tags:
            dimension, reference = geo_tags['GPSLatitude'], geo_tags['GPSLatitudeRef']
            latitude = self._get_decimal_coordinate(dimension, reference)

            dimension, reference = geo_tags['GPSLongitude'], geo_tags['GPSLongitudeRef']
            longitude = self._get_decimal_coordinate(dimension, reference)

        return latitude, longitude

    def get_tag(self, tag):
        """
        Specific tag value from exif info getter.

        :param tag: exif info tag name
        :return: value of a specific tag
        """
        if tag in self._exif:
            return self._exif[tag]

    @property
    def orientation(self):
        """Returns orientation tag value."""
        orientation_tag = 'Orientation'
        return self.get_tag(orientation_tag)

    @property
    def date_time(self):
        """Returns image datetime taken."""
        date_time_original_number_tag = 36867
        date_time = self.get_tag(date_time_original_number_tag)
        if not date_time:
            date_time_original_string_tag = 'DateTimeOriginal'
            date_time = self.get_tag(date_time_original_string_tag)
        return date_time
