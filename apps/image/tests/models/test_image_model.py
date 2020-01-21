from django.test import TestCase

from apps.image.models import ImageModel


class TestImageModel(TestCase):
    fixtures = ['apps/users/fixtures/test_data.json', 'apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = ImageModel.objects.create()

    def test_image_is_assigned_slug_on_creation(self):
        self.assertIsNotNone(self.model_instance.slug)
        self.assertIs(self.model_instance.slug.isnumeric(), True)

    def test_image_published_manager(self):
        model_query_set_all = ImageModel.objects.all()
        model_query_set_published = ImageModel.published.all()

        self.assertIs(model_query_set_all.count() == model_query_set_published.count(), False)

        for model_instance in model_query_set_published:
            self.assertIs(model_instance.status == ImageModel.PUBLISHED, True)
