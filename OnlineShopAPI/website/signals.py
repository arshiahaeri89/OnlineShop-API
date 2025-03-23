import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImage


@receiver(post_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    folder_path = os.path.dirname(instance.image.path)
    if instance.image and instance.image.name and instance.image.storage.exists(instance.image.name):
        instance.image.delete(save=False)

    if os.path.isdir(folder_path) and not os.listdir(folder_path):
        os.rmdir(folder_path)
