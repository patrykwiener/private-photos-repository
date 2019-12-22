from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.test_image_post_view_base import TestImagePostViewBase


class TestImagePostDeleteView(TestImagePostViewBase):
    fixtures = TestImagePostViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super(TestImagePostDeleteView, cls).setUpTestData()
        cls.image_post = ImageModel.published.filter(user=cls.user).first()

    def test_delete_denies_anonymous(self):
        response = self.client.get(reverse('image:image-post-delete', args=[self.image_post.slug]))
        self.assertEqual(response.status_code, 302)

    def test_delete_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('image:image-post-delete', args=[self.image_post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_post_delete.html')
        self.assertEqual(response.context['object'], self.image_post)

    def test_delete_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('image:image-post-delete', args=[self.image_post.slug]))

        self.assertEqual(response.status_code, 302)
        self.assertRaises(self.image_post.DoesNotExist, lambda: ImageModel.published.get(id=self.image_post.id))
