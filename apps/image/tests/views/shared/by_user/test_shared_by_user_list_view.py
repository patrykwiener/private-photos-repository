from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_view_base import TestImageViewBase


class TestSharedByUserListView(TestImageViewBase):
    fixtures = TestImageViewBase.fixtures + ['apps/image/fixtures/test_data_shared.json']

    @property
    def view_url(self):
        return reverse('image:shared-by-user')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_query_set = ImageModel.published.filter(sharedimagemodel__image__user=cls.user)

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_shared_by_user_list_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_by_user_image_list.html')
        self.assertCountEqual(response.context['object_list'], self.image_query_set)

    def test_shared_by_user_by_tag_list_get(self):
        self.login()
        tag = 'mountains'
        response = self.client.get(reverse('image:shared-by-user-by-tag', args=[tag]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_by_user_image_list.html')
        self.assertCountEqual(response.context['object_list'], self.image_query_set.filter(tags__slug=tag))

    def test_shared_by_user_by_person_list_get(self):
        self.login()
        person = 'anna-wojdan'
        response = self.client.get(reverse('image:shared-by-user-by-person', args=[person]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_by_user_image_list.html')
        self.assertCountEqual(response.context['object_list'], self.image_query_set.filter(facemodel__person__slug=person))
