from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.image.forms.image_upload_form import ImageUploadForm
from apps.image.services.image_processing.recognition import Recognition
from apps.image.services.image_upload_service import ImageUploadService
from apps.image.views.image_post.image_post_creation.image_creation_base import ImageCreationBase


class ImageUpload(ImageCreationBase):
    form_class = ImageUploadForm
    template_name = 'image/image_upload.html'
    success_url = reverse_lazy('image:image-post-create')

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super(ImageUpload, self).dispatch(request, *args, **kwargs)
        if self.get_draft_if_exists():
            return redirect(self.get_success_url())
        return dispatch_result

    def form_valid(self, form):
        data = form.cleaned_data
        image_model = ImageUploadService(self.request.user, data['image']).upload()
        Recognition(image_model).execute()
        return super(ImageUpload, self).form_valid(form)
