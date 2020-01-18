from apps.image.tests.views.mixins.test_single_object_view_mixin import TestSingleObjectViewMixin


class TestDeleteViewMixin(TestSingleObjectViewMixin):

    def test_post(self):
        self.login()
        model_instance = self.get_model_instance()
        response = self.client.post(self.get_view_url())

        self.assertEqual(response.status_code, 302)
        self.assertRaisesMessage(
            model_instance.DoesNotExist,
            'ImageModel matching query does not exist.',
            lambda: model_instance.__class__.objects.get(id=model_instance.id)
        )
