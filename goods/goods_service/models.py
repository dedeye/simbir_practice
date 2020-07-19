from django.db import models
from sortedm2m.fields import SortedManyToManyField
from django.dispatch import receiver
import os


class AdvertTag(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Advert(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=300, blank=True)
    contacts = models.TextField(max_length=200, blank=False)
    price = models.PositiveIntegerField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    tags = SortedManyToManyField(AdvertTag)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()

    class Meta:
        ordering = ["id"]


class AdvertImage(models.Model):
    file = models.FileField(upload_to="img")
    advert = models.ForeignKey(Advert, related_name="image", on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]


# delete file on disk after deleting in db
@receiver(models.signals.post_delete, sender=AdvertImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
