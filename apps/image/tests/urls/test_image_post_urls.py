from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.image.views.download_image import ImageDownload
from apps.image.views.image_post.image_post_creation.image_post_create import ImagePostCreate
from apps.image.views.image_post.image_post_creation.image_upload import ImageUpload
from apps.image.views.image_post.image_post_delete import ImagePostDelete
from apps.image.views.image_post.image_post_detail import ImagePostDetail
from apps.image.views.image_post.image_post_edit import ImagePostEdit
from apps.image.views.image_post.image_post_list import ImagePostList
from apps.image.views.image_post.image_post_share import ImagePostShare


class TestImagePostUrls(SimpleTestCase):
    VALID_SLUG = 'some-slug'
    VALID_NUMERIC_SLUG = '111111111111'

    def test_list_url_resolves(self):
        url = reverse('image:image-post-list')
        self.assertEqual(resolve(url).func.view_class, ImagePostList)

    def test_list_by_slug_url_resolves(self):
        url = reverse('image:image-post-list-by-slug', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostList)

    def test_list_by_person_url_resolves(self):
        url = reverse('image:image-post-list-by-person', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostList)

    def test_upload_url_resolves(self):
        url = reverse('image:image-upload')
        self.assertEqual(resolve(url).func.view_class, ImageUpload)

    def test_create_url_resolves(self):
        url = reverse('image:image-post-create')
        self.assertEqual(resolve(url).func.view_class, ImagePostCreate)

    def test_detail_url_resolves(self):
        url = reverse('image:image-post-detail', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostDetail)

    def test_edit_url_resolves(self):
        url = reverse('image:image-post-edit', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostEdit)

    def test_delete_url_resolves(self):
        url = reverse('image:image-post-delete', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostDelete)

    def test_share_person_url_resolves(self):
        url = reverse('image:image-post-share', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImagePostShare)

    def test_download_person_url_resolves(self):
        url = reverse('image:image-download', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageDownload)
