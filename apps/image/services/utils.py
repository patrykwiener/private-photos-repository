import numpy as np


class NumpyListConverter:

    @staticmethod
    def to_list(numpy_array):
        return numpy_array.tolist()

    @staticmethod
    def to_numpy_array(list_instance):
        return np.asarray(list_instance)

    @classmethod
    def to_numpy_arrays(cls, lists):
        return [cls.to_numpy_array(list_instance) for list_instance in lists]
