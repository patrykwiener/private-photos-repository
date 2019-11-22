from PIL.ExifTags import TAGS, GPSTAGS


class PictureExifInfo:

    def __init__(self, exif):
        self._exif = self._get_labeled_exif(exif)

    @staticmethod
    def _get_labeled_exif(exif):
        for key, value in exif.items():
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
    def create(cls, pil_image):
        exif = getattr(pil_image, '_getexif', lambda: None)()
        if exif:
            return cls(exif)

    @property
    def geo_tags(self):
        gps_info_tag = 'GPSInfo'
        if gps_info_tag in self._exif:
            gps_tags = {}
            for gps_key, gps_tag in GPSTAGS.items():
                if gps_key in self._exif[gps_info_tag]:
                    gps_tags[gps_tag] = self._exif[gps_info_tag][gps_key]

            return gps_tags

    @property
    def coordinates(self):
        geo_tags = self.geo_tags
        latitude, longitude = None, None
        if geo_tags:
            dimension, reference = geo_tags['GPSLatitude'], geo_tags['GPSLatitudeRef']
            latitude = self._get_decimal_coordinate(dimension, reference)

            dimension, reference = geo_tags['GPSLongitude'], geo_tags['GPSLongitudeRef']
            longitude = self._get_decimal_coordinate(dimension, reference)

        return latitude, longitude

    def get_tag(self, tag):
        if tag in self._exif:
            return self._exif[tag]

    @property
    def orientation(self):
        orientation_tag = 'Orientation'
        return self.get_tag(orientation_tag)

    @property
    def date_time(self):
        date_time_original_number_tag = 36867
        if not self.get_tag(date_time_original_number_tag):
            date_time_original_string_tag = 'DateTimeOriginal'
            return self.get_tag(date_time_original_string_tag)
