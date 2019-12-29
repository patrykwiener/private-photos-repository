from apps.image.tests.views.mixins.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixins.components.model_query_set_mixin import ModelQuerySetMixin
from apps.image.tests.views.mixins.components.template_mixin import TemplateMixin


class TestModelQuerySetViewMixin(TestImageViewMixin, TemplateMixin, ModelQuerySetMixin):

    def test_list_get(self):
        self.login()
        response = self.client.get(self.get_view_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
        self.assertCountEqual(
            self.model_query_set,
            response.context['object_list']
        )
