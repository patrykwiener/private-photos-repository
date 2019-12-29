from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_detail_view_mixin import TestDetailViewMixin


class TestImagePostDetailView(TestDetailViewMixin, TestCase):
    fixtures = TestDetailViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_post_detail.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.filter(user=TestDetailViewMixin.user).first()
        cls.view_url = reverse('image:image-post-detail', args=[cls.model_instance.slug])
