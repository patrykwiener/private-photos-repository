from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_delete_view_mixin import TestDeleteViewMixin


class TestImagePostDeleteView(TestDeleteViewMixin, TestCase):
    fixtures = TestDeleteViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_post_delete.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.filter(user=TestDeleteViewMixin.user).first()
        cls.view_url = reverse('image:image-post-delete', args=[cls.model_instance.slug])
