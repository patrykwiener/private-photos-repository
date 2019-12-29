from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixin.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixin.test_list_view_mixin import TestListViewMixin


class TestImagePostListView(TestListViewMixin, TestCase):
    fixtures = TestImageViewMixin.fixtures + ['apps/image/fixtures/test_data.json']
    template = 'image/image_list.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_query_set = ImageModel.published.all()
        cls.view_url = reverse('image:image-post-list')
