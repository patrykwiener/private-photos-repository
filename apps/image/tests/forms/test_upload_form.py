import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.test import SimpleTestCase

from apps.image.forms.image_upload_form import ImageUploadForm
from private_photos_repository.settings import MEDIA_ROOT


class TestUploadForm(SimpleTestCase):

    def test_form_valid_data(self):
        image_path = os.path.join(MEDIA_ROOT, 'sample_data/images/test_image.jpg')
        with Image.open(image_path) as image:
            with BytesIO() as image_io:
                image.save(image_io, format='JPEG')
                content_image = ContentFile(image_io.getvalue(), name='test_image.jpg')

        form = ImageUploadForm(files={
            'image': content_image
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = ImageUploadForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
