from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from apps.image.forms import ImageUploadForm, CreateImagePostForm
from apps.image.models.face_model import FaceModel
from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel
from apps.image.services.face_recognition.recognition import Recognition
from apps.image.services.upload_image import UploadImage


class UploadImageBaseView(View):
    @staticmethod
    def get_draft_if_exists():
        return ImageModel.objects.filter(status=ImageModel.DRAFT)


class UploadImageView(UploadImageBaseView):
    form_class = ImageUploadForm
    template_name = 'image/upload.html'
    create_image_post_url = '/image/create-image-post'

    def get(self, request):
        if self.get_draft_if_exists():
            return redirect(self.create_image_post_url)
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):
        if self.get_draft_if_exists():
            return redirect(self.create_image_post_url)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_model = UploadImage(image).create_draft()
            Recognition(image_model).execute()

            return redirect(self.create_image_post_url)
        else:
            messages.error(request, 'Whoops... Check provided information.')
        return render(request, self.template_name, {
            'form': form,
        })


class CreateImagePostView(UploadImageBaseView):
    form_class = CreateImagePostForm
    template_name = '/image/create_image_post.html'
    upload_image_url = '/image/upload-image'

    def get(self, request):
        image_model_query = self.get_draft_if_exists()
        if not image_model_query:
            return redirect(self.upload_image_url)

        image_model = image_model_query.first()
        faces = FaceModel.objects.filter(image=image_model)

        form = CreateImagePostForm(faces=faces)

        return render(request, 'image/create_image_post.html', {
            'thumb': image_model.thumbnail,
            'faces': faces,
            'form': form,
        })

    def post(self, request):
        image_model_query = self.get_draft_if_exists()
        if image_model_query:
            image_model = image_model_query.first()
            faces = FaceModel.objects.filter(image=image_model)
            if 'cancel' in request.POST:
                image_model.delete()
            elif 'upload' in request.POST:
                form = CreateImagePostForm(request.POST, faces=faces)
                if form.is_valid():
                    for face in faces:
                        field_name = 'face_{}'.format(face.id)
                        face_name = form.cleaned_data[field_name]
                        face_name = ' '.join(face_name.split())
                        person = None
                        if face_name != "":
                            person, _ = RecognizedPersonModel.objects.get_or_create(full_name=face_name,
                                                                                    defaults={
                                                                                        'full_name': face_name
                                                                                    })
                        if face.person != person:
                            face.person = person
                            face.save()

                    image_model.status = ImageModel.PUBLISHED
                    image_model.save()
                else:
                    messages.error(request, 'Whoops... Check provided information.')
        return redirect(self.upload_image_url)
