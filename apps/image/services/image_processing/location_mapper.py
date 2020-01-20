"""
This module contains LocationMapper tool class providing faces in pictures locations mapping.
"""
from typing import List, Tuple


class LocationMapper:
    """Tool class providing faces in pictures locations mapping."""

    @classmethod
    def to_original_image(cls,
                          locations: List[Tuple[int]],
                          original_pic_size: Tuple[int],
                          pic_size: Tuple[int]) -> List[Tuple[int]]:
        """
        Maps provided locations to their original values.

        :param locations: face coordinates to map
        :param original_pic_size: original size of picture
        :param pic_size: locations to map image size
        :return: mapped to original values locations
        """
        factor = original_pic_size[0] / pic_size[0]
        return cls._map_locations(locations, factor)

    @classmethod
    def _map_locations(cls, locations: List[Tuple[int]], factor: float) -> List[Tuple[int]]:
        """
        Performs locations mapping.

        :param locations: locations to map
        :param factor: computed factor by which all location components will be multiplied
        :return: mapped locations
        """
        mapped_locations = []
        for location in locations:
            mapped_locations.append(tuple([int(coordinate * factor) for coordinate in location]))
        return mapped_locations
