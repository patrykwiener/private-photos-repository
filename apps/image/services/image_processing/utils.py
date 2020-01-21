"""
This module contains NumpyListConverter tool class providing utils for conversion between
numpy arrays and Python's lists.
"""
import numpy as np


class NumpyListConverter:
    """Util class providing conversion between numpy arrays and Python's lists."""

    @staticmethod
    def to_list(numpy_array):
        """Converts numpy array to list."""
        return numpy_array.tolist()

    @staticmethod
    def to_numpy_array(list_instance):
        """Converts list to numpy array."""
        return np.asarray(list_instance)

    @classmethod
    def to_numpy_arrays(cls, lists):
        """Converts list of lists to list of numpy arrays."""
        return [cls.to_numpy_array(list_instance) for list_instance in lists]
