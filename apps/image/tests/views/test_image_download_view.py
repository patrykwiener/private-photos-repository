import os
from io import BytesIO

from PIL import Image, ImageChops
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImageDownloadView(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.get(user=cls.user, id=1)

    @staticmethod
    def get_bbox_difference(img1, img2):
        return ImageChops.difference(img1, img2).getbbox()

    def test_share_denies_anonymous(self):
        response = self.client.get(reverse('image:image-download', args=[self.image_post.slug]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('image:image-download', args=[self.image_post.slug]))
        self.assertEqual(response.status_code, 302)

    def test_share_get(self):
        self.login()

        response = self.client.get(reverse('image:image-download', args=[self.image_post.slug]))

        self.assertEqual(response.status_code, 200)

        file_name = os.path.basename(self.image_post.image.name)
        response_content_disposition = 'attachment; filename={}'.format(file_name)
        self.assertEqual(response.get('Content-Disposition'), response_content_disposition)

        with BytesIO(response.content) as response_bytes_io:
            self.assertGreater(len(response_bytes_io.read()), 0)

            with Image.open(response_bytes_io) as response_pil:
                with Image.open(self.image_post.image.path) as reference_pil:
                    self.assertTrue(self.get_bbox_difference(response_pil, reference_pil) is None)
