from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_view_mixin import TestImageViewMixin


class TestSharedListView(TestImageViewMixin):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data_shared.json']

    @property
    def view_url(self):
        return reverse('image:shared')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_query_set = ImageModel.published.filter(sharedimagemodel__recipient=cls.user)

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_shared_list_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_image_list.html')
        self.assertCountEqual(response.context['object_list'], self.image_query_set)

    def test_shared_list_by_tag_get(self):
        self.login()
        tag = 'mountains'
        response = self.client.get(reverse('image:shared-by-tag', args=[tag]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_image_list.html')
        self.assertCountEqual(response.context['object_list'], self.image_query_set.filter(tags__slug=tag))

    def test_shared_list_by_person_get(self):
        self.login()
        person = 'patryk-wiener'
        response = self.client.get(reverse('image:shared-by-person', args=[person]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_image_list.html')
        self.assertCountEqual(response.context['object_list'],
                              self.image_query_set.filter(facemodel__person__slug=person))
