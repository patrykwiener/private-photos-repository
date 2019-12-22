from datetime import datetime
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_view_mixin import TestImageViewMixin


class TestImagePostEditView(TestImageViewMixin):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.get(user=cls.user, id=1)

    @property
    def view_url(self):
        return reverse('image:image-post-edit', args=[self.image_post.slug])

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_edit_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_create.html')
        self.assertEqual(response.context['object'], self.image_post)

    def test_edit_post_cancel(self):
        self.login()

        response = self.client.post(self.view_url, {
            'cancel': 'Cancel'
        })

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.image_post.slug]))

    def test_edit_post_no_changes(self):
        self.login()

        person_names = [str(face.person) for face in self.image_post.facemodel_set.all()]
        latitude = self.image_post.latitude
        longitude = self.image_post.longitude
        body = self.image_post.body
        tags = self.image_post.tags
        datetime_taken = self.image_post.datetime_taken

        response = self.client.post(self.view_url, {
            'upload': 'Upload',
            'face_1': person_names[0],
            'face_2': person_names[1],
            'tags': ', '.join([tag.name for tag in tags.all()]),
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
        self.assertURLEqual(response.url, reverse('image:image-post-detail', args=[self.image_post.slug]))

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
