import datetime

from django.db import models
from django.utils.timezone import now


class ImageModel(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
    )

    image = models.ImageField(upload_to='images/',
                              default='pic_folder/None/no-img.jpg')
    thumbnail = models.ImageField(upload_to='thumbnails/',
                                  default='pic_folder/None/no-img.jpg')

    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    date_time_taken = models.DateTimeField(default=None, blank=True, null=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=DRAFT)
