"""
This module contains RecognitionResult class responsible for interpretation of face recognition
results.
"""
from operator import itemgetter
from typing import List, Tuple, Optional

from apps.image.models.recognized_person_model import RecognizedPersonModel


class RecognitionResult:
    """This class is responsible for interpretation of face recognition results."""

    def __init__(self, people: List[RecognizedPersonModel], results: List[bool],
                 distances: List[float]):
        """
        Initializes class props.

        :param people: list of defined people in user's images
        :param results: list of comparison boolean result for each face
        :param distances: list of distances between face under recognition and other faces
        """
        self._people = people
        self._results = results
        self._distances = distances

    @property
    def recognized_person(self) -> Optional[RecognizedPersonModel]:
        """Returns the most similar person to a person in a picture founded by minimum distance."""
        recognized_people = self.recognized_people
        if not recognized_people:
            return None
        person_index = 0
        distance_index = 1
        return min(recognized_people, key=itemgetter(distance_index))[person_index]

    @property
    def recognized_people(self) -> List[Tuple[RecognizedPersonModel, float]]:
        """Filters result returning list of only recognized persons with their distances."""
        return [(person, distance) for person, result, distance in self.result if result]

    @property
    def result(self) -> List[Tuple[RecognizedPersonModel, bool, float]]:
        """Returns zipped lists of corresponding values."""
        return list(zip(self._people, self._results, self._distances))
