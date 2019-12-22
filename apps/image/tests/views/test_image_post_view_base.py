import abc

from django.test import TestCase

from apps.users.models import CustomUser


class TestImagePostViewBase(TestCase, metaclass=abc.ABCMeta):
    fixtures = ['apps/users/fixtures/test_data.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.get(id=1)

    def login(self):
        self.client.force_login(self.user)
