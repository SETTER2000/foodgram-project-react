import os

from django.db import models
from django.dispatch import receiver
from app.models import Recipes


@receiver(models.signals.post_delete, sender=Recipes)
def delete_file(sender, instance, *args, **kwargs):
    """Deletes image files on `post_delete`"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
