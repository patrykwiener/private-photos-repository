from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImagePostDetailView(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.filter(user=cls.user).first()

    def test_detail_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-detail', args=[self.image_post.slug]))
        self.assertEqual(response.status_code, 302)

    def test_detail_get(self):
        self.login()
        response = self.client.get(reverse('image:image-post-detail', args=[self.image_post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_detail.html')
        self.assertEqual(response.context['object'], self.image_post)
