"""
This module contains RecognizedPeopleService service class saving recognized people to database.
"""
from typing import List, Dict

from apps.image.models.face_model import FaceModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class RecognizedPeopleService:
    """Service class saving recognized people to database."""

    def __init__(self, faces: List[FaceModel], cleaned_data: Dict):
        """
        Initializes class props.

        :param faces: list of FaceModel objects representing faces in a picture
        :param cleaned_data: ImagePostCreateForm form cleaned data
        """
        self.faces = faces
        self._cleaned_data = cleaned_data

    def save_recognized_face(self):
        """
        Saves recognized faces. Associates faces in FaceModel table and theirs recognized people
        stored in RecognizedPersonModel table. If needed creates new RecognizedPersonModel basing
        on the form cleaned data.
        """
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
