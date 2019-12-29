from apps.image.tests.views.mixin.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixin.test_single_object_mixin import TestSingleObjectMixin
from apps.image.tests.views.mixin.test_template_mixin import TestTemplateMixin


class TestDetailViewMixin(TestImageViewMixin, TestTemplateMixin, TestSingleObjectMixin):

    def test_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context['object'], self.model_instance)
