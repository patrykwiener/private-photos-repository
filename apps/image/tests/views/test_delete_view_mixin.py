import abc

from django.core.exceptions import ImproperlyConfigured

from apps.image.tests.views.test_image_view_mixin import TestImageViewMixin


class TestDeleteViewMixin(TestImageViewMixin):
    model_instance = None
    template = None

    def test_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context['object'], self.get_model_instance())

    def test_post(self):
        self.login()
        model_instance = self.get_model_instance()
        response = self.client.post(self.view_url)

        self.assertEqual(response.status_code, 302)
        self.assertRaises(model_instance.DoesNotExist,
                          lambda: model_instance.__class__.objects.get(id=model_instance.id))

    def get_model_instance(self):
        if self.model_instance is None:
            raise ImproperlyConfigured(
                '{cls} is missing a model instance. '
                'Define {cls}.model_instance or override {cls}.get_model_instance().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.model_instance

    def get_template(self):
        if self.template is None:
            raise ImproperlyConfigured(
                '{cls} is missing a template. '
                'Define {cls}.template or override {cls}.get_template().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.template
