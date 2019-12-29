import os
import shutil

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_image_view_mixin import TestImageViewMixin
from private_photos_repository.settings import MEDIA_ROOT


class TestImageUploadView(TestImageViewMixin, TestCase):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_upload.html'

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT += 'test'
        cls.view_url = reverse('image:image-upload')

    def test_upload_get(self):
        self.login()
        response = self.client.get(self.get_view_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_upload_redirect_when_draft_exists(self):
        self.login()
        ImageModel.objects.create(user=self.user)

        expected_url = reverse('image:image-post-create')
        response = self.client.get(self.get_view_url())

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_upload_post(self):
        self.login()
        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image.jpg')
        with open(image_path, 'rb') as image:
            response = self.client.post(self.get_view_url(), {
                'image': image
            })

        image_query_set = ImageModel.objects.filter(user=self.user, status=ImageModel.DRAFT)

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-create'))
        self.assertTrue(image_query_set.exists())

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()
