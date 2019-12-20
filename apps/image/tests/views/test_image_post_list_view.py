from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImagePostListView(TestImagePostViewBase):

    def test_list_denies_anonymous(self):
        response = self._client.get(reverse('image:image-post-list'))
        self.assertEqual(response.status_code, 302)

    def test_list_get(self):
        self._client.force_login(self._user)
        response = self._client.get(reverse('image:image-post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.published.all(),
            response.context['object_list']
        )

    def test_list_by_tag_get(self):
        self._client.force_login(self._user)
        slug = 'sun'
        response = self._client.get(reverse('image:image-post-list-by-slug', args=[slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(tags__slug=slug),
            response.context['object_list']
        )

    def test_list_by_person_get(self):
        self._client.force_login(self._user)
        person = 'patryk-wiener'
        response = self._client.get(
            reverse('image:image-post-list-by-person', args=[person])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            ImageModel.objects.filter(facemodel__person__slug=person, user=self._user),
            response.context['object_list']
        )
