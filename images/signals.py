from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ImageConversion


@receiver(post_delete, sender=ImageConversion)
def delete_image_file(sender, instance, **kwargs):
    if instance.converted_image:
        instance.converted_image.delete(save=False)
