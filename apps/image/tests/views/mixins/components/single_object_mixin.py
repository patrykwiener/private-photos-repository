from django.core.exceptions import ImproperlyConfigured


class SingleObjectMixin:
    model_instance = None

    def get_model_instance(self):
        if self.model_instance is None:
            raise ImproperlyConfigured(
                '{cls} is missing a model instance. '
                'Define {cls}.model_instance or override {cls}.get_model_instance().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.model_instance
