from django.test import TestCase

from apps.image.forms.image_post_share_form import ImagePostShareForm
from apps.image.models import ImageModel
from apps.users.models import CustomUser


class TestShareForm(TestCase):
    fixtures = [
        'apps/users/fixtures/test_data.json',
        'apps/image/fixtures/test_data_shared.json'
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.get(username='testadmin')
        cls.test_user = CustomUser.objects.get(username='testuser')
        cls.shared_image = ImageModel.published.get(user=cls.user, sharedimagemodel__recipient=cls.test_user)
        cls.shared_initial = {
            'user': cls.user,
            'image': cls.shared_image,
        }

    def test_form_valid_data(self):
        data = {
            'email': self.test_user.email
        }

        unshared_image = ImageModel.objects.exclude(sharedimagemodel__recipient=self.test_user).first()

        initial = {
            'user': self.user,
            'image': unshared_image
        }

        form = ImagePostShareForm(
            data=data,
            initial=initial
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_data_share_with_yourself(self):
        data = {
            'email': self.user.email
        }
        form = ImagePostShareForm(
            data=data,
            initial=self.shared_initial
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('You cannot share an image with yourself.' in form.errors['email'])

    def test_form_invalid_data_fake_email(self):
        data = {
            'email': 'face_email@domain.com'
        }
        form = ImagePostShareForm(
            data=data,
            initial=self.shared_initial
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('User with the given email does not exist.' in form.errors['email'])

    def test_form_invalid_data_share_the_same_image(self):
        data = {
            'email': self.test_user.email
        }

        form = ImagePostShareForm(
            data=data,
            initial=self.shared_initial
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('You\'re already sharing this image with the given user.' in form.errors['email'])
