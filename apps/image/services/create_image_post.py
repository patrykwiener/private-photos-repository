from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class CreateImagePost:

    def __init__(self, image_model, faces, cleaned_data):
        self._image_model = image_model
        self._faces = faces
        self._cleaned_data = cleaned_data

    def save_recognized_face(self):
        for face in self._faces:
            field_name = 'face_{}'.format(face.id)
            face_name = self._cleaned_data[field_name]
            face_name = ' '.join(face_name.split())
            person = None
            if face_name != "":
                person, _ = RecognizedPersonModel.objects.get_or_create(full_name=face_name,
                                                                        defaults={
                                                                            'full_name': face_name
                                                                        })
            if face.person != person:
                face.person = person
                face.save()

    def execute(self):
        self.save_recognized_face()
        self.publish()
        self.add_location()
        self.add_body()
        self._image_model.save()

    def publish(self):
        self._image_model.status = ImageModel.PUBLISHED

    def add_location(self):
        latitude = self._cleaned_data['latitude']
        longitude = self._cleaned_data['longitude']
        if latitude and longitude:
            self._image_model.latitude = latitude
            self._image_model.longitude = longitude

    def add_body(self):
        self._image_model.body = self._cleaned_data['body']
