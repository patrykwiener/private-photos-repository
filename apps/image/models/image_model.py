"""
This module contains PublishedManager providing only published image posts QuerySet object and ImageModel
class representing an image post.
"""
from django.urls import reverse
from django.db import models
from django.utils.crypto import get_random_string
from taggit.managers import TaggableManager

from apps.users.models import CustomUser


class PublishedManager(models.Manager):
    """Represents ImageModel class additional manager for only published image posts."""

    def get_queryset(self):
        """
        QuerySet object for only published image posts getter.

        :return: QuerySet object for published image posts
        """
        return super().get_queryset().filter(status='published')


class ImageModel(models.Model):
    """Represents an image post."""

    class Meta:
        ordering = ('-publish',)

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, blank=True, null=True)

    image = models.ImageField(upload_to='images/',
                              default='pic_folder/None/no-img.jpg',
                              )
    thumbnail = models.ImageField(upload_to='thumbnails/',
                                  default='pic_folder/None/no-img.jpg')

    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    datetime_taken = models.DateTimeField(default=None, blank=True, null=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=DRAFT)

    body = models.TextField(max_length=1024, default='')

    tags = TaggableManager()

    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    publish = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs):
        """Sets unique slug and saves an object to database."""
        self._set_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Absolute url getter"""
        return reverse('image:image-post-detail',
                       args=[
                           self.slug
                       ])

    def _set_slug(self):
        """Sets 12 numeral unique slug."""
        if not self.slug:
            slug_duplication = True
            while slug_duplication:
                self.slug = get_random_string(12, '0123456789')
                if ImageModel.objects.filter(slug=self.slug).count() == 0:
                    slug_duplication = False
