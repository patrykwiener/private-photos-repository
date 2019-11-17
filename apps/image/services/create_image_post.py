from apps.image.models.image_model import ImageModel
from apps.image.models.recognized_person_model import RecognizedPersonModel


class CreateImagePost:

    @staticmethod
    def save_recognized_face(face, face_name):
        face_name = ' '.join(face_name.split())
        person = None
        if face_name != "":
            person, _ = RecognizedPersonModel.objects.get_or_create(full_name=face_name,
                                                                    defaults={
                                                                        'full_name': face_name
                                                                    })
        if face.person != person:
            face.person = person
            face.save()

    @staticmethod
    def publish(image_model):
        image_model.status = ImageModel.PUBLISHED
        image_model.save()
