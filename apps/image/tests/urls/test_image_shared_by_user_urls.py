from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.image.views.shared.by_user.image_shared_by_user_delete import ImageSharedByUserDelete
from apps.image.views.shared.by_user.image_shared_by_user_list import ImageSharedByUserList


class TestImageSharedByUserUrls(SimpleTestCase):
    VALID_SLUG = 'some-slug'
    VALID_NUMERIC_SLUG = '111111111111'
    VALID_RECIPIENT_ID = '1'

    def test_list_url_resolves(self):
        url = reverse('image:shared-by-user')
        self.assertEqual(resolve(url).func.view_class, ImageSharedByUserList)

    def test_list_by_slug_url_resolves(self):
        url = reverse('image:shared-by-user-by-tag', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedByUserList)

    def test_list_by_person_url_resolves(self):
        url = reverse('image:shared-by-user-by-person', args=[self.VALID_SLUG])
        self.assertEqual(resolve(url).func.view_class, ImageSharedByUserList)

    def test_delete_url_resolves(self):
        url = reverse('image:shared-by-user-delete', args=[
            self.VALID_NUMERIC_SLUG,
            self.VALID_RECIPIENT_ID
        ])
        self.assertEqual(resolve(url).func.view_class, ImageSharedByUserDelete)
