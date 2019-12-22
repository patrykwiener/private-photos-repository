from django.urls import reverse

from apps.image.models import ImageModel, SharedImageModel
from apps.image.tests.views.test_image_view_base import TestImageViewBase
from apps.users.models import CustomUser


class TestImagePostShareView(TestImageViewBase):
    fixtures = TestImageViewBase.fixtures + ['apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.image_post = ImageModel.published.get(user=cls.user, id=1)

    @property
    def view_url(self):
        return reverse('image:image-post-share', args=[self.image_post.slug])

    def test_denies_anonymous(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)

    def test_share_get(self):
        self.login()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_share.html')
        self.assertEqual(response.context['object'], self.image_post)

    def test_share_post_blank(self):
        self.login()

        response = self.client.post(self.view_url, {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_share.html')
        self.assertEqual(response.context['object'], self.image_post)
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_share_post_invalid(self):
        self.login()

        response = self.client.post(self.view_url, {
            'email': 'fake_email'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_share.html')
        self.assertEqual(response.context['object'], self.image_post)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_share_post(self):
        self.login()

        second_user = CustomUser.objects.get(username='testuser')
        response = self.client.post(self.view_url, {
            'email': second_user.email
        })

        self.assertEqual(response.status_code, 302)

        shared_query_set = SharedImageModel.objects.filter(recipient=second_user, image=self.image_post)
        self.assertTrue(shared_query_set.exists())
