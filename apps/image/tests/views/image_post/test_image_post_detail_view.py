from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_view_base import TestImageViewBase


class TestImagePostDetailView(TestImageViewBase):
    fixtures = TestImageViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.filter(user=cls.user).first()

    @property
    def view_url(self):
        return reverse('image:image-post-detail', args=[self.image_post.slug])

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_detail_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_detail.html')
        self.assertEqual(response.context['object'], self.image_post)
