from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_single_object_view_mixin import TestSingleObjectViewMixin


class TestImagePostDetailView(TestSingleObjectViewMixin, TestCase):
    fixtures = TestSingleObjectViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_post_detail.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.filter(user=TestSingleObjectViewMixin.user).first()
        cls.view_url = reverse('image:image-post-detail', args=[cls.model_instance.slug])
