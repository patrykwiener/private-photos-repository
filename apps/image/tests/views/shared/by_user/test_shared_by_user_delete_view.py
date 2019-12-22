from django.urls import reverse

from apps.image.models import SharedImageModel
from apps.image.tests.views.test_image_view_base import TestImageViewBase


class TestSharedByUserDeleteView(TestImageViewBase):
    fixtures = TestImageViewBase.fixtures + ['apps/image/fixtures/test_data_shared.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.shared_image = SharedImageModel.objects.filter(image__user=cls.user).first()

    @property
    def view_url(self):
        return reverse('image:shared-by-user-delete', args=[self.shared_image.image.slug, self.shared_image.recipient.id])

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/shared_by_user_image_delete.html')
        self.assertEqual(response.context['object'], self.shared_image)

    def test_delete_post(self):
        self.login()

        response = self.client.post(self.view_url)

        self.assertEqual(response.status_code, 302)
        self.assertRaises(self.shared_image.DoesNotExist, lambda: SharedImageModel.objects.get(id=self.shared_image.id))

