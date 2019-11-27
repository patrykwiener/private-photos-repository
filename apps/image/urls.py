from django.urls import path

from apps.image import views

app_name = 'image'

urlpatterns = [
    path('', views.ImagePostListView.as_view(), name='image-post-list'),
    path('image-upload/', views.UploadImageView.as_view(), name='image-upload'),
    path('image-post-create/', views.CreateImagePostView.as_view(), name='image-post-create'),
    path('detail/<slug:slug>/', views.ImagePostDetailView.as_view(), name="image-detail"),
    path('edit/<slug:slug>/', views.ImagePostEditView.as_view(), name="image-edit"),
    path('delete/<slug:slug>/', views.ImagePostDeleteView.as_view(), name="image-delete"),
]
