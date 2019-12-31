from copy import deepcopy
from typing import List
import face_recognition
from apps.image.services.image_processing.picture import PictureForRecognition
from apps.image.services.image_processing.utils import NumpyListConverter
from apps.image.services.image_processing.recognition_result import RecognitionResult
from apps.image.models.face_model import FaceModel
from apps.image.models.image_model import ImageModel
from apps.image.services.image_processing.location_mapper import LocationMapper


class Recognition:

    def __init__(self, image_model: ImageModel):
        self._image_model = image_model

    def execute(self):

        pic_for_recognition = PictureForRecognition.create_pic(self._image_model.thumbnail)
        faces = self.find_faces(pic_for_recognition)
        pic_for_recognition.close()

        face_query = FaceModel.objects.filter(image__user=self._image_model.user)
        known_faces = face_query.recognized_faces()

        if known_faces:
            faces = self.recognize_faces(known_faces, faces)

        for face in faces:
            face.save()
        return faces

    def find_faces(self, picture):
        locations = face_recognition.face_locations(picture.pic_np_gray_scale, model='cnn')
        encodings = face_recognition.face_encodings(picture.pic_np, locations)

        locations = LocationMapper.to_original_image(locations, picture.original_size, picture.pic_size)

        faces = []
        for location, encoding in zip(locations, encodings):
            faces.append(
                FaceModel(image=self._image_model, encoding=NumpyListConverter.to_list(encoding), location=location))
        return faces

    @classmethod
    def recognize_faces(cls, known_faces, faces: List[FaceModel], tolerance=0.6) -> List[FaceModel]:
        faces = deepcopy(faces)
        for face in faces:
            recognition_result = cls.compare_with_unknown(known_faces, face, tolerance)
            face.person = recognition_result.recognized_person
        return faces

    @staticmethod
    def compare_with_unknown(known_faces, face: FaceModel, tolerance=0.6) -> RecognitionResult:
        distances = face_recognition.face_distance(NumpyListConverter.to_numpy_arrays(known_faces.encodings()),
                                                   NumpyListConverter.to_numpy_array(face.encoding))
        results = list(distances <= tolerance)
        return RecognitionResult(known_faces.people(), results, distances)
