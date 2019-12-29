from apps.image.tests.views.mixin.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixin.test_single_object_mixin import TestSingleObjectMixin
from apps.image.tests.views.mixin.test_template_mixin import TestTemplateMixin


class TestDeleteViewMixin(TestImageViewMixin, TestTemplateMixin, TestSingleObjectMixin):

    def test_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context['object'], self.get_model_instance())

    def test_post(self):
        self.login()
        model_instance = self.get_model_instance()
        response = self.client.post(self.view_url)

        self.assertEqual(response.status_code, 302)
        self.assertRaises(model_instance.DoesNotExist,
                          lambda: model_instance.__class__.objects.get(id=model_instance.id))