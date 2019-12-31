from unittest import mock

from django.db.models.signals import post_save, post_delete
from django.test import TestCase

from apps.image.models import FaceModel, RecognizedPersonModel
from apps.image.models.signals import delete_person_when_unreferenced


class TestFaceModel(TestCase):
    fixtures = ['apps/users/fixtures/test_data.json', 'apps/image/fixtures/test_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.faces = FaceModel.objects.all()

    def test_original_person(self):
        model_instance = FaceModel.objects.get(id=1)
        original_person = model_instance.person
        another_person = RecognizedPersonModel.objects.get(id=2)
        model_instance.person = another_person
        model_instance.save()

        self.assertEqual(original_person, model_instance.original_person)

    def test_face_model_custom_manager_encodings(self):
        encodings = self.faces.encodings()

        for encoding, face in zip(encodings, self.faces):
            self.assertEqual(encoding, face.encoding)

    def test_face_model_custom_manager_people(self):
        people = self.faces.people()

        for person, face in zip(people, self.faces):
            self.assertEqual(person, face.person)

    def test_face_model_custom_manager_recognized_faces(self):
        recognized_faces = self.faces.recognized_faces()

        for recognized_face, face in zip(recognized_faces, self.faces.exclude(person__isnull=True)):
            self.assertEqual(recognized_face, face)

    def test_signal_delete_person_when_unreferenced_post_save(self):
        with mock.patch('apps.image.models.signals.delete_person_when_unreferenced_post_save',
                        autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=FaceModel)
            model_instance = FaceModel.objects.get(id=1)
            another_person = RecognizedPersonModel.objects.get(id=2)
            model_instance.person = another_person
            model_instance.save()

        self.assertTrue(mocked_handler.called)
        self.assertEqual(mocked_handler.call_count, 1)

    def test_signal_delete_person_when_unreferenced_post_delete(self):
        with mock.patch('apps.image.models.signals.delete_person_when_unreferenced_post_delete',
                        autospec=True) as mocked_handler:
            post_delete.connect(mocked_handler, sender=FaceModel)
            model_instance = FaceModel.objects.get(id=1)
            model_instance.delete()

        self.assertTrue(mocked_handler.called)
        self.assertEqual(mocked_handler.call_count, 1)

    def test_delete_person_when_unreferenced(self):
        person = RecognizedPersonModel.objects.create(
            full_name='Some Guy'
        )

        delete_person_when_unreferenced(person)

        self.assertFalse(RecognizedPersonModel.objects.filter(id=person.id).exists())
