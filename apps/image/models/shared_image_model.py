from django.db import models

from apps.image.models.image_model import ImageModel
from apps.users.models import CustomUser


class SharedImageModel(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
