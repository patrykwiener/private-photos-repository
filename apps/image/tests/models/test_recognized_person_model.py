from django.test import TestCase

from apps.image.models import RecognizedPersonModel


class TestRecognizedPersonModel(TestCase):

    def test_is_assigned_slug_on_creation(self):
        person = RecognizedPersonModel.objects.create(
            full_name='Some Guy'
        )
        
        self.assertEqual(person.slug, 'some-guy')
