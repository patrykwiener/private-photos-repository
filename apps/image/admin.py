"""This module contains image app admin page definition."""
from django.contrib import admin
from taggit.admin import Tag

admin.site.unregister(Tag)
