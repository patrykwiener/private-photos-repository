from django.urls import reverse

from apps.image.models import ImageModel, SharedImageModel
from apps.image.tests.views.test_image_view_base import TestImageViewBase


class TestSharedDeleteView(TestImageViewBase):
    fixtures = TestImageViewBase.fixtures + ['apps/image/fixtures/test_data_shared.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.shared_image = SharedImageModel.objects.filter(recipient=cls.user).first()

    @property
    def view_url(self):
        return reverse('image:shared-delete', args=[self.shared_image.image.slug])

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_image_delete.html')
        self.assertEqual(response.context['object'], self.shared_image)

    def test_delete_post(self):
        self.login()

        response = self.client.post(self.view_url)

        self.assertEqual(response.status_code, 302)
        self.assertRaises(self.shared_image.DoesNotExist, lambda: SharedImageModel.objects.get(id=self.shared_image.id))
