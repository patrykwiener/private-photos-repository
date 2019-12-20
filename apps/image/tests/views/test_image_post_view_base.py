import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, Client

from apps.users.models import CustomUser

settings.MEDIA_ROOT += 'test'


class TestImagePostViewBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/test_data.json', verbosity=0)

        cls._user = CustomUser.objects.get(id=1)

        cls._client = Client()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)
        super(TestImagePostViewBase, cls).tearDownClass()
