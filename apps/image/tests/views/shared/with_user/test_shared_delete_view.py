from django.test import TestCase
from django.urls import reverse

from apps.image.models import SharedImageModel
from apps.image.tests.views.mixins.test_delete_view_mixin import TestDeleteViewMixin


class TestSharedDeleteView(TestDeleteViewMixin, TestCase):
    fixtures = TestDeleteViewMixin.fixtures + ['apps/image/fixtures/test_data_shared.json']
    template = 'image/shared_image_delete.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = SharedImageModel.objects.filter(recipient=TestDeleteViewMixin.user).first()
        cls.view_url = reverse('image:shared-delete', args=[cls.model_instance.image.slug])
