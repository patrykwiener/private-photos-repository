from operator import itemgetter
from typing import List, Tuple

from apps.image.models.recognized_person_model import RecognizedPersonModel


class RecognitionResult:
    def __init__(self, people: List[RecognizedPersonModel], results: List[bool], distances: List[float]):
        self._people = people
        self._results = results
        self._distances = distances

    @property
    def recognized_person(self):
        recognized_people = self.recognized_people
        if not recognized_people:
            return None
        person_index = 0
        distance_index = 1
        return max(recognized_people, key=itemgetter(distance_index))[person_index]

    @property
    def recognized_people(self) -> List[Tuple[RecognizedPersonModel, float]]:
        return [(person, distance) for person, result, distance in
                zip(self._people, self._results, self._distances) if result]

    @property
    def result(self):
        return list(zip(self._people, self._results, self._distances))
