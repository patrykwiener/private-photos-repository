from apps.image.tests.views.test_image_view_mixin import TestImageViewMixin


class TestListViewMixin(TestImageViewMixin):
    model_list = None
    template = None
    model = None

    def test_list_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image/image_list.html')
        self.assertCountEqual(
            self.model_list.__class__.published.all(),
            response.context['object_list']
        )

