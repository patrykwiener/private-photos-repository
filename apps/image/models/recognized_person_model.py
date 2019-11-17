from django.db import models


class RecognizedPersonModel(models.Model):
    full_name = models.CharField(max_length=100)
