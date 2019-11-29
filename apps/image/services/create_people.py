from typing import List

from apps.image.models.face_model import FaceModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class CreatePeople:

    def __init__(self, faces: List[FaceModel], cleaned_data):
        self.faces = faces
        self._cleaned_data = cleaned_data

    def save_recognized_face(self):
        for face in self.faces:
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
