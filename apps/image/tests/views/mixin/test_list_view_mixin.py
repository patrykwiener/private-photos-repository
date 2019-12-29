from apps.image.tests.views.mixin.test_image_view_mixin import TestImageViewMixin
from apps.image.tests.views.mixin.test_model_query_set_mixin import TestModelQuerySetMixin
from apps.image.tests.views.mixin.test_template_mixin import TestTemplateMixin


class TestListViewMixin(TestImageViewMixin, TestTemplateMixin, TestModelQuerySetMixin):
    template = None

    @property
    def view_url_by_person(self):
        return '{}person/'.format(self.view_url)

    @property
    def view_url_by_tag(self):
        return '{}tag/'.format(self.view_url)

    def test_list_get(self):
        self.login()
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertCountEqual(
            self.model_query_set,
            response.context['object_list']
        )

    def test_list_by_tag_get(self):
        self.login()
        tag = 'sun'
        response = self.client.get(
            self.view_url_by_tag + tag + '/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertCountEqual(
            self.model_query_set.filter(tags__slug=tag),
            response.context['object_list']
        )

    def test_list_by_person_get(self):
        self.login()
        person = 'patryk-wiener'
        response = self.client.get(
            self.view_url_by_person + person + '/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertCountEqual(
            self.model_query_set.filter(facemodel__person__slug=person, user=self.user),
            response.context['object_list']
        )
