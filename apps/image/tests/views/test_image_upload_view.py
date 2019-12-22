import os
import shutil

from django.conf import settings
from django.urls import reverse
from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase
from private_photos_repository.settings import MEDIA_ROOT


class TestImageUploadView(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        settings.MEDIA_ROOT += 'test'
        super(TestImageUploadView, cls).setUpTestData()

    def test_upload_denies_anonymous(self):
        response = self.client.get(reverse('image:image-upload'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('image:image-upload'))
        self.assertEqual(response.status_code, 302)

    def test_upload_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('image:image-upload'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_upload.html')

    def test_upload_redirect_when_draft_exists(self):
        self.client.force_login(self.user)
        ImageModel.objects.create(user=self.user)

        expected_url = reverse('image:image-post-create')
        response = self.client.get(reverse('image:image-upload'))

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_upload_post(self):
        self.client.force_login(self.user)
        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image.jpg')
        with open(image_path, 'rb') as image:
            response = self.client.post(reverse('image:image-upload'), {
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
        super(TestImagePostViewBase, cls).tearDownClass()
