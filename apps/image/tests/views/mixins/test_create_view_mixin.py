from django.core.exceptions import ImproperlyConfigured

from apps.image.tests.views.mixins.test_single_object_view_mixin import TestSingleObjectViewMixin


class TestCreateViewMixin(TestSingleObjectViewMixin):
    cancel_url = None

    def test_cancel(self):
        self.login()

        response = self.client.post(self.get_view_url(), {
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
