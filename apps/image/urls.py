from django.urls import path

from apps.image import views

app_name = 'image'

urlpatterns = [
    path('upload-image/', views.UploadImageView.as_view(), name='upload_image'),
    path('create-image-post/', views.CreateImagePostView.as_view(), name='finish_upload')
]
