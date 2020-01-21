"""This module contains ImagePostEdit class view responsible for image post edition handling."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView

from apps.image.forms.image_post_create_form import ImagePostCreateForm
from apps.image.models.image_model import ImageModel
from apps.image.services.recognized_people_service import RecognizedPeopleService


class ImagePostEdit(LoginRequiredMixin, UpdateView):
    """Represents image post edit view."""
    form_class = ImagePostCreateForm
    template_name = 'image/image_post_create.html'
    model = ImageModel

    def get_object(self, queryset=None):
        """
        Finds ImageModel object to edit by URL slug. Also sets form initial values such as faces on
        an image, latitude and longitude of the image taken place.

        :return: ImageModel object to edit
        """
        slug = self.kwargs.get('slug')
        object_to_update = get_object_or_404(self.model, user=self.request.user, slug=slug,
                                             status=self.model.PUBLISHED)
        self.initial = {
            'faces': object_to_update.facemodel_set.all(),
            'latitude': object_to_update.latitude,
            'longitude': object_to_update.longitude,
        }
        return object_to_update

    def post(self, request, *args, **kwargs):
        """
        Performs image post edition when 'upload' is in request. Redirects on 'cancel'.

        :param request: POST request
        :return: image post edition response
        """
        if 'cancel' in request.POST:
            return redirect(self.get_object().get_absolute_url())
        elif 'upload' in request.POST:
            return super().post(request, *args, **kwargs)
        raise NotImplementedError('Request contains no submitted button name.')

    def form_valid(self, form):
        """
        Updates recognized faces when valid.

        :param form: ImagePostCreateForm submitted form
        :return: image post edition response
        """
        RecognizedPeopleService(self.object.facemodel_set.all(),
                                form.cleaned_data).save_recognized_face()
        messages.success(self.request, 'The post has been updated!')
        return super().form_valid(form)
