import os

from django.urls import reverse
from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase
from private_photos_repository.settings import MEDIA_ROOT


class TestImageUploadView(TestImagePostViewBase):

    def test_upload_denies_anonymous(self):
        response = self._client.get(reverse('image:image-upload'))
        self.assertEqual(response.status_code, 302)
        response = self._client.post(reverse('image:image-upload'))
        self.assertEqual(response.status_code, 302)

    def test_upload_get(self):
        self._client.force_login(self._user)
        response = self._client.get(reverse('image:image-upload'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_upload.html')

    def test_upload_redirect_when_draft_exists(self):
        self._client.force_login(self._user)
        ImageModel.objects.create(user=self._user)

        expected_url = reverse('image:image-post-create')
        response = self._client.get(reverse('image:image-upload'))

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_upload_post(self):
        self._client.force_login(self._user)
        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image.jpg')
        with open(image_path, 'rb') as image:
            response = self._client.post(reverse('image:image-upload'), {
                'image': image
            })

        image_query_set = ImageModel.objects.filter(user=self._user, status=ImageModel.DRAFT)

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-create'))
        self.assertTrue(image_query_set.exists())
