from django.core.exceptions import ImproperlyConfigured

from apps.users.models import CustomUser


class TestImageViewMixin:
    view_url = None
    client = None
    fixtures = ['apps/users/fixtures/test_data.json']
    user = CustomUser.objects.get(username='testadmin')

    def login(self):
        self.client.force_login(self.user)

    def test_denies_anonymous(self):
        response = self.client.get(self.get_view_url())
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.get_view_url())
        self.assertEqual(response.status_code, 302)

    def get_view_url(self):
        if self.view_url is None:
            raise ImproperlyConfigured(
                '{cls} is missing a view url. '
                'Define {cls}.view_url or override {cls}.get_view_url().'.format(
                    cls=self.__class__.__name__
                )
            )
        return self.view_url
