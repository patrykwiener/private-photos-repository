import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.services.image_upload_service import ImageUploadService
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase
from private_photos_repository.settings import MEDIA_ROOT


class TestImagePostCreateViews(TestImagePostViewBase):

    # @staticmethod
    # def create_image_post(user):
    #     image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                               'test_data/../../../../fixtures/sample_data/test_image.jpg')
    #
    #     with open(image_path, 'rb') as file:
    #         uploaded_image = SimpleUploadedFile(name='test_image.jpg', content=file.read(),
    #                                             content_type='image/jpeg')
    #
    #     image_post = ImageUploadService(user, uploaded_image).upload()
    #     Recognition(image_post).execute()
    #
    #     data = {
    #         'latitude': 0.0,
    #         'longitude': 0.0,
    #         'body': 'Sample Body',
    #         'tags': ['sampletag1', 'sampletag2'],
    #     }
    #
    #     ImagePostCreateService(image_post, data).execute()
    #
    #     data = {
    #         'face_1': 'Sample Name1',
    #         'face_2': 'Sample Name2'
    #     }
    #
    #     RecognizedPeopleService(image_post.facemodel_set.all(), data).save_recognized_face()
    #
    #     return image_post

    def create_image_post_draft(self):
        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image1.jpg')
        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(name='test_image.jpg', content=file.read(), content_type='image/jpeg')
        return ImageUploadService(self._user, image).upload()

    def test_create_denies_anonymous(self):
        response = self._client.get(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)
        response = self._client.post(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)

    def test_create_get(self):
        self._client.force_login(self._user)

        image_post = self.create_image_post_draft()
        response = self._client.get(reverse('image:image-post-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_create.html')
        self.assertEqual(response.context['object'], image_post)

    def test_create_redirect_when_draft_does_not_exists(self):
        self._client.force_login(self._user)

        expected_url = reverse('image:image-upload')
        response = self._client.get(reverse('image:image-post-create'))

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_create_post_cancel(self):
        self._client.force_login(self._user)

        response = self._client.post(reverse('image:image-post-create'), {
            'cancel': 'Cancel'
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-upload'))

    def test_create_post(self):
        self._client.force_login(self._user)

        image_post = self.create_image_post_draft()
        response = self._client.post(reverse('image:image-post-create'), {
            'upload': 'Upload'
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[image_post.slug]))

        image_query_set = ImageModel.published.filter(user=self._user, id=image_post.id)
        self.assertTrue(image_query_set.exists())

        image_post.status = ImageModel.PUBLISHED
        self.assertEqual(image_post, image_query_set.first())
