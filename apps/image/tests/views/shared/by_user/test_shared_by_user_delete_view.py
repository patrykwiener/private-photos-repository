from django.test import TestCase
from django.urls import reverse

from apps.image.models import SharedImageModel
from apps.image.tests.views.mixins.test_delete_view_mixin import TestDeleteViewMixin


class TestSharedByUserDeleteView(TestDeleteViewMixin, TestCase):
    fixtures = TestDeleteViewMixin.fixtures + ['apps/image/fixtures/test_data_shared.json']
    template = 'image/shared_by_user_image_delete.html'

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = SharedImageModel.objects.filter(image__user=cls.user).first()
        cls.view_url = reverse('image:shared-by-user-delete', args=[
            cls.model_instance.image.slug,
            cls.model_instance.recipient.id
        ])
