from django.core.exceptions import ImproperlyConfigured

from apps.image.tests.views.mixins.components.single_object_mixin import SingleObjectMixin
from apps.image.tests.views.mixins.components.template_mixin import TemplateMixin
from apps.image.tests.views.mixins.test_image_view_mixin import TestImageViewMixin


class TestCreateViewMixin(TestImageViewMixin, TemplateMixin, SingleObjectMixin):
    cancel_url = None

    def test_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
        self.assertEqual(response.context['object'], self.get_model_instance())

    def test_cancel(self):
        self.login()

        response = self.client.post(self.view_url, {
            'cancel': 'Cancel'
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, self.get_cancel_url())

    def get_cancel_url(self):
        if self.cancel_url is None:
            raise ImproperlyConfigured(
                '{cls} is missing a cancel_url. '
                'Define {cls}.cancel_url or override {cls}.get_cancel_url().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.cancel_url
