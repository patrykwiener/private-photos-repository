"""This module contains image app url definitions."""

from django.urls import path, re_path

from apps.image.views.download_image import ImageDownload
from apps.image.views.image_post.image_post_creation.image_post_create import ImagePostCreate
from apps.image.views.image_post.image_post_creation.image_upload import ImageUpload
from apps.image.views.image_post.image_post_delete import ImagePostDelete
from apps.image.views.image_post.image_post_detail import ImagePostDetail
from apps.image.views.image_post.image_post_edit import ImagePostEdit
from apps.image.views.image_post.image_post_list import ImagePostList
from apps.image.views.image_post.image_post_share import ImagePostShare
from apps.image.views.shared.with_user.image_shared_delete import ImageSharedDelete
from apps.image.views.shared.with_user.image_shared_detail import ImageSharedDetail
from apps.image.views.shared.with_user.image_shared_list import ImageSharedList
from apps.image.views.shared.by_user.image_shared_by_user_delete import ImageSharedByUserDelete
from apps.image.views.shared.by_user.image_shared_by_user_list import ImageSharedByUserList

app_name = 'image'
NUMERIC_SLUG_RE = r'^(?P<slug>\d+)/$'

urlpatterns = [
    # image post list view
    path('', ImagePostList.as_view(), name='image-post-list'),
    path('tag/<slug:tag_slug>/', ImagePostList.as_view(), name='image-post-list-by-slug'),
    path('person/<slug:person_slug>/', ImagePostList.as_view(), name='image-post-list-by-person'),
    path('upload/', ImageUpload.as_view(), name='image-upload'),
    path('new/', ImagePostCreate.as_view(), name='image-post-create'),

    # image post operations
    re_path(r'^(?P<slug>\d+)/$', ImagePostDetail.as_view(), name='image-post-detail'),
    re_path(r'^(?P<slug>\d+)/edit/$', ImagePostEdit.as_view(), name='image-post-edit'),
    re_path(r'^(?P<slug>\d+)/delete/$', ImagePostDelete.as_view(), name='image-post-delete'),
    re_path(r'^(?P<slug>\d+)/share/$', ImagePostShare.as_view(), name='image-post-share'),
    re_path(r'^(?P<slug>\d+)/download/$', ImageDownload.as_view(), name='image-download'),

    # shared with user
    path('shared/', ImageSharedList.as_view(), name='shared'),
    path('shared/tag/<slug:tag_slug>/', ImageSharedList.as_view(), name='shared-by-tag'),
    path('shared/person/<slug:person_slug>/', ImageSharedList.as_view(), name='shared-by-person'),
    re_path(r'^shared/(?P<slug>\d+)/delete/$', ImageSharedDelete.as_view(), name='shared-delete'),
    re_path(r'^shared/(?P<slug>\d+)/$', ImageSharedDetail.as_view(), name='shared-detail'),

    # shared by user
    path('shared-by-user/', ImageSharedByUserList.as_view(), name='shared-by-user'),
    path(
        'shared-by-user/tag/<slug:tag_slug>/',
        ImageSharedByUserList.as_view(),
        name='shared-by-user-by-tag'
    ),
    path(
        'shared-by-user/person/<slug:person_slug>/',
        ImageSharedByUserList.as_view(),
        name='shared-by-user-by-person'
    ),
    re_path(
        r'^shared-by-user/(?P<slug>\d+)-(?P<recipient_id>\d+)/delete/$',
        ImageSharedByUserDelete.as_view(),
        name='shared-by-user-delete'
    ),

]
