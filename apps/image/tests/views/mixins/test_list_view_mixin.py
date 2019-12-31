from apps.image.tests.views.mixins.test_model_query_set_view_mixin import TestModelQuerySetViewMixin


class TestListViewMixin(TestModelQuerySetViewMixin):

    @property
    def view_url_by_person(self):
        return '{}person/'.format(self.get_view_url())

    @property
    def view_url_by_tag(self):
        return '{}tag/'.format(self.get_view_url())

    def test_list_by_tag_get(self):
        self.login()
        tag = 'sun'
        response = self.client.get(
            self.view_url_by_tag + tag + '/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template())
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
        self.assertTemplateUsed(response, self.get_template())
        self.assertCountEqual(
            self.model_query_set.filter(facemodel__person__slug=person, user=self.user),
            response.context['object_list']
        )
