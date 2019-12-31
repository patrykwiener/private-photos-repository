from apps.image.models.image_model import ImageModel


class ImagePostCreateService:

    def __init__(self, image_model: ImageModel, data):
        self._image_model = image_model
        self._data = data

    def execute(self, save=True):
        self.publish()
        self.add_location()
        self.add_datetime_taken()
        self.add_body()
        self.add_tags()
        if save:
            self._image_model.save()

    def publish(self):
        self._image_model.status = ImageModel.PUBLISHED

    def add_location(self):
        self._image_model.latitude = self._data['latitude']
        self._image_model.longitude = self._data['longitude']

    def add_body(self):
        self._image_model.body = self._data['body']

    def add_datetime_taken(self):
        if not self._image_model.datetime_taken:
            self._image_model.datetime_taken = self._data['datetime_taken']

    def add_tags(self):
        self._image_model.tags.set(*self._data['tags'])
