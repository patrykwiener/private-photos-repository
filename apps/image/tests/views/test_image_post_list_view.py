from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImagePostListView(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    def test_list_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-list'))
        self.assertEqual(response.status_code, 302)

    def test_list_get(self):
        self.login()
        response = self.client.get(reverse('image:image-post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.published.all(),
            response.context['object_list']
        )

    def test_list_by_tag_get(self):
        self.login()
        slug = 'sun'
        response = self.client.get(reverse('image:image-post-list-by-slug', args=[slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(tags__slug=slug),
            response.context['object_list']
        )

    def test_list_by_person_get(self):
        self.login()
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