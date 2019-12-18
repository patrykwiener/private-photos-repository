import os
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from apps.image.models.image_model import ImageModel
from apps.image.services.image_upload_service import ImageUploadService
from apps.users.models import CustomUser
from private_photos_repository.settings import MEDIA_ROOT


class TestImagePostViews(TestCase):

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

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/test_data.json', verbosity=0)

        cls.user = CustomUser.objects.get(id=1)

        cls.image_post = ImageModel.objects.get(id=1)

        cls.client = Client()

        settings.MEDIA_ROOT += 'test'

    def test_list_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-list'))
        self.assertEqual(response.status_code, 302)

    def test_list_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('image:image-post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.published.all(),
            response.context['object_list']
        )

    def test_list_by_tag_get(self):
        self.client.force_login(self.user)
        slug = 'sun'
        response = self.client.get(reverse('image:image-post-list-by-slug', args=[slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(tags__slug=slug),
            response.context['object_list']
        )

    def test_list_by_person_get(self):
        self.client.force_login(self.user)
        person = 'patryk-wiener'
        response = self.client.get(
            reverse('image:image-post-list-by-person', args=[person])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(facemodel__person__slug=person, user=self.user),
            response.context['object_list']
        )

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

    def test_create_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)

    def test_create_get(self):
        self.client.force_login(self.user)

        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image1.jpg')
        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(name='test_image.jpg', content=file.read(), content_type='image/jpeg')
        image_post = ImageUploadService(self.user, image).upload()

        response = self.client.get(reverse('image:image-post-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_create.html')
        self.assertEqual(response.context['object'], image_post)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)
        super(TestImagePostViews, cls).tearDownClass()
