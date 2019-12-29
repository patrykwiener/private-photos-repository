from django.core.exceptions import ImproperlyConfigured


class ModelQuerySetMixin:
    model_query_set = None

    def get_model_query_set(self):
        if self.model_query_set is None:
            raise ImproperlyConfigured(
                '{cls} is missing a model_query_set. '
                'Define {cls}.model_query_set or override {cls}.get_model_query_set().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.model_query_set
