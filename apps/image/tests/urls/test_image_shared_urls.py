from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.image.views.shared.with_user.image_shared_delete import ImageSharedDelete
from apps.image.views.shared.with_user.image_shared_detail import ImageSharedDetail
from apps.image.views.shared.with_user.image_shared_list import ImageSharedList


class TestImageSharedUrls(SimpleTestCase):
    VALID_SLUG = 'some-slug'
    VALID_NUMERIC_SLUG = '111111111111'

    def test_list_url_resolves(self):
        url = reverse('image:shared')
        self.assertEqual(resolve(url).func.view_class, ImageSharedList)

    def test_list_by_slug_url_resolves(self):
        url = reverse('image:shared-by-tag', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedList)

    def test_list_by_person_url_resolves(self):
        url = reverse('image:shared-by-person', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedList)

    def test_delete_url_resolves(self):
        url = reverse('image:shared-delete', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedDelete)

    def test_detail_url_resolves(self):
        url = reverse('image:shared-detail', args=[self.VALID_NUMERIC_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedDetail)
