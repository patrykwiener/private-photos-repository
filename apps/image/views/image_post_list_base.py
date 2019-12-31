from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from apps.image.models.recognized_person_model import RecognizedPersonModel


class ImagePostListBase(LoginRequiredMixin, ListView):
    paginate_by = 100

    def __init__(self):
        super().__init__()
        self.tag = None
        self.person = None

    def filter_by_tag(self):
        tag_slug = 'tag_slug'
        if tag_slug in self.kwargs:
            self.tag = get_object_or_404(Tag, slug=self.kwargs[tag_slug])
            self.queryset = self.queryset.filter(tags__in=[self.tag])

    def filter_by_person(self):
        person_slug = 'person_slug'
        if person_slug in self.kwargs:
            self.person = get_object_or_404(RecognizedPersonModel, slug=self.kwargs[person_slug])
            self.queryset = self.queryset.filter(facemodel__person__in=[self.person])

    def get(self, request, *args, **kwargs):
        self.filter_by_tag()
        self.filter_by_person()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['person'] = self.person
        return context
