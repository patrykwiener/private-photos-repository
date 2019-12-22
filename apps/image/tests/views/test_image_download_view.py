import os
from io import BytesIO

from PIL import Image, ImageChops
from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_view_mixin import TestImageViewMixin


class TestImageDownloadView(TestImageViewMixin, TestCase):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.get(user=cls.user, id=1)

    @property
    def view_url(self):
        return reverse('image:image-download', args=[self.image_post.slug])

    @staticmethod
    def get_bbox_difference(img1, img2):
        return ImageChops.difference(img1, img2).getbbox()

    def test_share_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)

        file_name = os.path.basename(self.image_post.image.name)
        response_content_disposition = 'attachment; filename={}'.format(file_name)
        self.assertEqual(response.get('Content-Disposition'), response_content_disposition)

        with BytesIO(response.content) as response_bytes_io:
            self.assertGreater(len(response_bytes_io.read()), 0)

            with Image.open(response_bytes_io) as response_pil:
                with Image.open(self.image_post.image.path) as reference_pil:
                    self.assertTrue(self.get_bbox_difference(response_pil, reference_pil) is None)
