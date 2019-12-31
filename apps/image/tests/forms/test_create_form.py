from django.test import TestCase

from apps.image.forms.image_post_create_form import ImagePostCreateForm
from apps.image.models import FaceModel


class TestCreateForm(TestCase):
    fixtures = [
        'apps/users/fixtures/test_data.json',
        'apps/image/fixtures/test_data.json'
    ]

    @classmethod
    def setUpTestData(cls):
        faces = FaceModel.objects.all()
        latitude = 0
        longitude = 0
        cls.initial = {
            'faces': faces,
            'latitude': latitude,
            'longitude': longitude
        }

    def test_form_blank(self):
        form = ImagePostCreateForm(data={}, initial=self.initial)

        self.assertTrue(form.is_valid())

    def test_form_full_data(self):
        data = {
            'body': 'Sample Body',
            'datetime_taken': '1111-11-11 11:11',
            'tags': ['tag1, tag2'],
            'latitude': 1.1,
            'longitude': 1.1,
        }

        form = ImagePostCreateForm(data=data, initial=self.initial)

        self.assertTrue(form.is_valid())
