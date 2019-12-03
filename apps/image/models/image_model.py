from django.urls import reverse
from django.db import models
from taggit.managers import TaggableManager
from django.utils.crypto import get_random_string

from apps.users.models import CustomUser


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class ImageModel(models.Model):
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

    def get_absolute_url(self):
        return reverse('image:image-post-detail',
                       args=[
                           self.slug
                       ])

    def save(self, *args, **kwargs):
        self._set_slug()
        super(ImageModel, self).save(*args, **kwargs)

    def _set_slug(self):
        if not self.slug:
            slug_duplication = True
            while slug_duplication:
                self.slug = get_random_string(12, '0123456789')
                if ImageModel.objects.filter(slug=self.slug).count() == 0:
                    slug_duplication = False

    class Meta:
        ordering = ('-publish',)
