from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel, SharedImageModel
from apps.image.tests.views.mixins.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixins.test_single_object_view_mixin import TestSingleObjectViewMixin
from apps.users.models import CustomUser


class TestImagePostShareView(TestSingleObjectViewMixin, TestCase):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_share.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.get(user=cls.user, id=1)
        cls.view_url = reverse('image:image-post-share', args=[cls.model_instance.slug])

    def test_share_post_blank(self):
        self.login()

        response = self.client.post(self.get_view_url(), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
        self.assertEqual(response.context['object'], self.get_model_instance())
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_share_post_invalid(self):
        self.login()

        response = self.client.post(self.get_view_url(), {
            'email': 'fake_email'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
        self.assertEqual(response.context['object'], self.get_model_instance())
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_share_post(self):
        self.login()

        second_user = CustomUser.objects.get(username='testuser')
        response = self.client.post(self.get_view_url(), {
            'email': second_user.email
        })

        self.assertEqual(response.status_code, 302)

        shared_query_set = SharedImageModel.objects.filter(recipient=second_user, image=self.get_model_instance())
        self.assertTrue(shared_query_set.exists())
