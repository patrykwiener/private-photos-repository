from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from apps.image.models.face_model import FaceModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


def delete_person_when_unreferenced(person: RecognizedPersonModel):
    if person:
        if person.facemodel_set.count() == 0:
            person.delete()


@receiver(post_delete, sender=FaceModel)
def delete_person_when_unreferenced_post_delete(sender, instance: FaceModel, **kwargs):
    delete_person_when_unreferenced(instance.person)


@receiver(post_save, sender=FaceModel)
def delete_person_when_unreferenced_post_save(sender, instance: FaceModel, **kwargs):
    if instance.original_person != instance.person:
        delete_person_when_unreferenced(instance.original_person)
