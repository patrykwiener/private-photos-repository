import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from apps.image.models.image_model import ImageModel
from apps.image.services.image_post_create_service import ImagePostCreateService
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.image_upload_service import ImageUploadService
from apps.image.services.recognized_people_service import RecognizedPeopleService
from apps.users.models import CustomUser


class TestImagePostViews(TestCase):

    @staticmethod
    def create_image_post(user):
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data/test_image.jpg')

        with open(image_path, 'rb') as file:
            uploaded_image = SimpleUploadedFile(name='test_image.jpg', content=file.read(),
                                                content_type='image/jpeg')

        image_post = ImageUploadService(user, uploaded_image).upload()
        Recognition(image_post).execute()

        data = {
            'latitude': 0.0,
            'longitude': 0.0,
            'body': 'Sample Body',
            'tags': ['sampletag1', 'sampletag2'],
        }

        ImagePostCreateService(image_post, data).execute()

        data = {
            'face_1': 'Sample Name1',
            'face_2': 'Sample Name2'
        }

        RecognizedPeopleService(image_post.facemodel_set.all(), data).save_recognized_face()

        return image_post

    @classmethod
    def setUpTestData(cls):
        username = 'TestUser1'
        password = 'test123'
        email = 'testuser@domain.com'
        cls.user = CustomUser.objects.create(
            username=username,
            password=password,
            email=email,
        )

        cls.image_post = cls.create_image_post(cls.user)

        cls.client = Client()

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_GET(self):
        response = self.client.get(reverse('image:image-post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.all(),
            response.context['object_list']
        )

    def test_list_by_tag_GET(self):
        tag = self.image_post.tags.first()

        response = self.client.get(
            reverse('image:image-post-list-by-slug', args=[
                tag.name
            ])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(tags=tag),
            response.context['object_list']
        )

    def test_list_by_person_GET(self):
        face = self.image_post.facemodel_set.first()

        response = self.client.get(
            reverse('image:image-post-list-by-person', args=[
                face.person.slug
            ])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(facemodel=face),
            response.context['object_list']
        )
