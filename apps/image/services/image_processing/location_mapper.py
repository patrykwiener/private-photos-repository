from typing import List, Tuple


class LocationMapper:

    @classmethod
    def to_original_image(cls,
                          locations: List[Tuple[int]],
                          original_pic_size: Tuple[int],
                          pic_size: Tuple[int]) -> List[Tuple[int]]:
        factor = original_pic_size[0] / pic_size[0]
        return cls._map_locations(locations, factor)

    @classmethod
    def _map_locations(cls, locations: List[Tuple[int]], factor: float) -> List[Tuple[int]]:
        mapped_locations = []
        for location in locations:
            mapped_locations.append(tuple([int(coordinate * factor) for coordinate in location]))
        return mapped_locations
