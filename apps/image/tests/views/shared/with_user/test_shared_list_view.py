from django.test import TestCase
from django.urls import reverse

from apps.image.models import ImageModel
from apps.image.tests.views.mixins.test_list_view_mixin import TestListViewMixin


class TestSharedListView(TestListViewMixin, TestCase):
    fixtures = TestListViewMixin.fixtures + ['apps/image/fixtures/test_data_shared.json']
    template = 'image/shared_image_list.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_query_set = ImageModel.published.filter(sharedimagemodel__recipient=cls.user)
        cls.view_url = reverse('image:shared')
