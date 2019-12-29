from apps.image.tests.views.mixins.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixins.components.single_object_mixin import SingleObjectMixin
from apps.image.tests.views.mixins.components.template_mixin import TemplateMixin


class TestSingleObjectViewMixin(TestImageViewMixin, TemplateMixin, SingleObjectMixin):

    def test_get(self):
        self.login()

        response = self.client.get(self.get_view_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
        self.assertEqual(response.context.get('object'), self.get_model_instance())
