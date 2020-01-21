"""This module contains Recognition class performing face recognition on am image."""
from copy import deepcopy
from typing import List
import face_recognition

from apps.image.services.image_processing.picture import PictureForRecognition
from apps.image.services.image_processing.utils import NumpyListConverter
from apps.image.services.image_processing.recognition_result import RecognitionResult
from apps.image.models.face_model import FaceModel, FaceQuerySet
from apps.image.models.image_model import ImageModel
from apps.image.services.image_processing.location_mapper import LocationMapper


class Recognition:
    """Performs face recognition process."""

    def __init__(self, image_model: ImageModel):
        self._image_model = image_model

    def execute(self):
        """
        Performs face recognition on ImageModel object containing uploaded image. Uses
        face_recognition library with cnn method. Saves recognized faces to database.
        """
        pic_for_recognition = PictureForRecognition.create_pic(self._image_model.thumbnail)
        faces = self._find_faces(pic_for_recognition)
        pic_for_recognition.close()

        face_query = FaceModel.objects.filter(image__user=self._image_model.user)
        known_faces = face_query.recognized_faces()

        if known_faces:
            faces = self._recognize_faces(known_faces, faces)

        for face in faces:
            face.save()

    def _find_faces(self, picture: PictureForRecognition) -> List[FaceModel]:
        """
        Finds faces locations in the given picture. Generates face encodings. Maps faces
        locations to original image file size. Basing on found faces creates FaceModel objects.

        :param picture: shrunk uploaded image
        :return: list of founded faces
        """
        locations = face_recognition.face_locations(picture.pic_np_gray_scale, model='cnn')
        encodings = face_recognition.face_encodings(picture.pic_np, locations)

        locations = LocationMapper.to_original_image(locations, picture.original_size,
                                                     picture.pic_size)

        faces = []
        for location, encoding in zip(locations, encodings):
            faces.append(
                FaceModel(image=self._image_model, encoding=NumpyListConverter.to_list(encoding),
                          location=location))
        return faces

    @classmethod
    def _recognize_faces(cls, known_faces: FaceQuerySet, faces: List[FaceModel],
                         tolerance=0.6) -> List[FaceModel]:
        """
        Recognizes each face by comparing them with user's already known faces.

        :param known_faces: user's already known faces
        :param faces: found faces
        :param tolerance: threshold rejecting not similar faces
        :return: recognized faces
        """
        faces = deepcopy(faces)
        for face in faces:
            recognition_result = cls._compare_with_unknown(known_faces, face, tolerance)
            face.person = recognition_result.recognized_person
        return faces

    @staticmethod
    def _compare_with_unknown(known_faces: FaceQuerySet, face: FaceModel,
                              tolerance=0.6) -> RecognitionResult:
        """
        Compares unknown face with all known faces. Generates distances defining similarity of
        two faces. Distances are tested against the given tolerance. Creates RecognitionResult
        object containing recognition result.

        :param known_faces: all already known faces
        :param face: face to recognize
        :param tolerance: distances threshold
        :return: RecognitionResult object containing recognition result
        """
        distances = face_recognition.face_distance(
            NumpyListConverter.to_numpy_arrays(known_faces.encodings()),
            NumpyListConverter.to_numpy_array(face.encoding))
        results = list(distances <= tolerance)
        return RecognitionResult(known_faces.people(), results, distances)
