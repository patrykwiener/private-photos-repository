from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_create_view_mixin import TestCreateViewMixin


class TestImagePostEditView(TestCreateViewMixin, TestCase):
    fixtures = TestCreateViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_post_create.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.get(user=cls.user, id=1)
        cls.view_url = reverse('image:image-post-edit', args=[cls.model_instance.slug])
        cls.cancel_url = reverse('image:image-post-detail', args=[cls.model_instance.slug])

    def test_edit_post_no_changes(self):
        self.login()

        person_names = [str(face.person) for face in self.model_instance.facemodel_set.all()]
        latitude = self.model_instance.latitude
        longitude = self.model_instance.longitude
        body = self.model_instance.body
        tags = self.model_instance.tags
        datetime_taken = self.model_instance.datetime_taken

        response = self.client.post(self.view_url, {
            'upload': 'Upload',
            'face_1': person_names[0],
            'face_2': person_names[1],
            'tags': ', '.join([tag.name for tag in tags.all()]),
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.model_instance.slug]))

        image_query_set = ImageModel.published.filter(user=self.user, id=self.model_instance.id)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(latitude=latitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(longitude=longitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(body=body)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(datetime_taken__contains=datetime_taken.strftime("%Y-%m-%d %H:%M"))
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(tags__in=tags.all())
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(facemodel__person__full_name__in=person_names).distinct()
        self.assertTrue(image_query_set.exists())

    def test_edit_post_blank(self):
        self.login()

        response = self.client.post(self.view_url, {
            'upload': 'Upload',
            'face_1': '',
            'face_2': '',
            'latitude': '',
            'longitude': '',
            'body': '',
            'tags': '',
            'datetime_taken': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.model_instance.slug]))

        image_query_set = ImageModel.published.filter(user=self.user, id=self.model_instance.id)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(latitude=None)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(longitude=None)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(body='')
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(datetime_taken=None)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(tags=None)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(facemodel__person=None)
        self.assertTrue(image_query_set.exists())

    def test_edit_post(self):
        self.login()

        person_names = ['some person', 'another person']
        latitude = 50.3785
        longitude = 14.9706
        body = 'body test'
        tags = ['some tag', 'another_tag']
        datetime_taken = datetime.now()

        response = self.client.post(self.view_url, {
            'upload': 'Upload',
            'face_1': person_names[0],
            'face_2': person_names[1],
            'latitude': latitude,
            'longitude': longitude,
            'body': body,
            'tags': ', '.join(tags),
            'datetime_taken': datetime_taken.strftime("%Y-%m-%dT%H:%M"),
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.model_instance.slug]))

        image_query_set = ImageModel.published.filter(user=self.user, id=self.model_instance.id)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(latitude=latitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(longitude=longitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(body=body)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(datetime_taken__contains=datetime_taken.strftime("%Y-%m-%d %H:%M"))
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(tags__name__in=tags).distinct()
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(facemodel__person__full_name__in=person_names).distinct()
        self.assertTrue(image_query_set.exists())
