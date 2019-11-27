from django.db import models


class RecognizedPersonModel(models.Model):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name