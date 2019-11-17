from django.db import models


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
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=DRAFT)
