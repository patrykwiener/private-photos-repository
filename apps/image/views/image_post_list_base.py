"""
This module contains ImagePostListBase base class view for all image posts list views in image
app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from apps.image.models.recognized_person_model import RecognizedPersonModel


class ImagePostListBase(LoginRequiredMixin, ListView):
    """
    Base for all image posts list views in image app. Provides filtering image posts by tags
    and people on GET method.
    """
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.tag = None
        self.person = None

    def filter_by_tag(self):
        """Filters queryset (image posts) by tag slug stored in kwargs attribute."""
        tag_slug = 'tag_slug'
        if tag_slug in self.kwargs:
            self.tag = get_object_or_404(Tag, slug=self.kwargs[tag_slug])
            self.queryset = self.queryset.filter(tags__in=[self.tag])

    def filter_by_person(self):
        """Filters queryset (image posts) by person slug stored in kwargs attribute."""
        person_slug = 'person_slug'
        if person_slug in self.kwargs:
            self.person = get_object_or_404(RecognizedPersonModel, slug=self.kwargs[person_slug])
            self.queryset = self.queryset.filter(facemodel__person__in=[self.person])

    def get(self, request, *args, **kwargs):
        """Handles GET request. Applies filtering by tag and person if needed."""
        self.filter_by_tag()
        self.filter_by_person()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Returns context data. Appends tag and person objects to context data."""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['person'] = self.person
        return context
