from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_single_object_view_mixin import TestSingleObjectViewMixin


class TestSharedDetailView(TestSingleObjectViewMixin, TestCase):
    fixtures = TestSingleObjectViewMixin.fixtures + ['apps/image/fixtures/test_data_shared.json']
    template = 'image/shared_image_detail.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.published.filter(sharedimagemodel__recipient=cls.user).first()
        cls.view_url = reverse('image:shared-detail', args=[cls.model_instance.slug])
