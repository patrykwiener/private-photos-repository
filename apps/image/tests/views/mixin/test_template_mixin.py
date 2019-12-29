from django.core.exceptions import ImproperlyConfigured


class TestTemplateMixin:
    template = None

    def get_template(self):
        if self.template is None:
            raise ImproperlyConfigured(
                '{cls} is missing a template. '
                'Define {cls}.template or override {cls}.get_template().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.template
