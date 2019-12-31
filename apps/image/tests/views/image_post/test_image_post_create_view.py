from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_create_view_mixin import TestCreateViewMixin


class TestImagePostCreateViews(TestCreateViewMixin, TestCase):
    fixtures = TestCreateViewMixin.fixtures + ['apps/image/fixtures/test_data_with_draft.json']
    template = 'image/image_post_create.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.objects.get(user=cls.user, status=ImageModel.DRAFT)
        cls.view_url = reverse('image:image-post-create')
        cls.cancel_url = reverse('image:image-upload')
        cls.success_url = reverse('image:image-post-detail', args=[cls.model_instance.slug])
        cls.image_post = ImageModel.objects.get(user=cls.user, status=ImageModel.DRAFT)

    def test_create_redirect_when_draft_does_not_exists(self):
        self.login()
        self.image_post.delete()

        expected_url = reverse('image:image-upload')
        response = self.client.get(self.get_view_url())

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_create_post_blank(self):
        self.login()

        response = self.client.post(self.get_view_url(), {
            'upload': 'Upload',
            'face_1': '',
            'face_2': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, self.success_url)

        image_query_set = ImageModel.published.filter(user=self.user, id=self.image_post.id)
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

    def test_create_post(self):
        self.login()

        person_names = ['some person', 'another person']
        latitude = 50.3785
        longitude = 14.9706
        body = 'body test'
        tags = ['some tag', 'another_tag']
        datetime_taken = datetime.now()

        response = self.client.post(self.get_view_url(), {
            'upload': 'Upload',
            'face_1': person_names[0],
            'face_2': person_names[1],
            'latitude': latitude,
            'longitude': longitude,
            'body': body,
            'tags': ', '.join(tags),
            'datetime_taken': datetime_taken.strftime("%Y-%m-%d %H:%M"),
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, self.success_url)

        image_query_set = ImageModel.published.filter(user=self.user, id=self.image_post.id)
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
