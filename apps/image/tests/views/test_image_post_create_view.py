from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from apps.image.models import ImageModel, RecognizedPersonModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImagePostCreateViews(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data_with_draft.json']

    @classmethod
    def setUpTestData(cls):
        super(TestImagePostCreateViews, cls).setUpTestData()
        cls.image_post = ImageModel.objects.get(user=cls.user, status=ImageModel.DRAFT)

    def test_create_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('image:image-post-create'))
        self.assertEqual(response.status_code, 302)

    def test_create_get(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('image:image-post-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_create.html')
        self.assertEqual(response.context['object'], self.image_post)

    def test_create_redirect_when_draft_does_not_exists(self):
        self.client.force_login(self.user)
        self.image_post.delete()

        expected_url = reverse('image:image-upload')
        response = self.client.get(reverse('image:image-post-create'))

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, expected_url)

    def test_create_post_cancel(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('image:image-post-create'), {
            'cancel': 'Cancel'
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-upload'))

    def test_create_post_blank(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('image:image-post-create'), {
            'upload': 'Upload',
            'face_1': '',
            'face_2': '',
        })
        self.image_post.status = ImageModel.PUBLISHED
        for face in self.image_post.facemodel_set.all():
            face.person = None

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.image_post.slug]))

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
        self.client.force_login(self.user)

        person_names = ['Patryk Wiener', 'Anna Wojdan']

        latitude = 50.3785
        longitude = 14.9706
        body = 'body test'
        tags = ['some tag', 'another_tag']
        datetime_taken = datetime.now()

        response = self.client.post(reverse('image:image-post-create'), {
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
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.image_post.slug]))

        image_query_set = ImageModel.published.filter(user=self.user, id=self.image_post.id)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(latitude=latitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(longitude=longitude)
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(body=body)
        self.assertTrue(image_query_set.exists())

        datetime_taken = make_aware(datetime_taken)
        image_query_set = image_query_set.filter(datetime_taken__contains=datetime_taken.strftime("%Y-%m-%d %H:%M"))
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(tags__name__in=tags).distinct()
        self.assertTrue(image_query_set.exists())

        image_query_set = image_query_set.filter(facemodel__person__full_name__in=person_names).distinct()
        self.assertTrue(image_query_set.exists())
