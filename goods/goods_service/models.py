from django.db import models
from django.dispatch import receiver
from safedelete.models import SafeDeleteModel
from sortedm2m.fields import SortedManyToManyField


class AdvertTag(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Advert(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=500, blank=True)
    contacts = models.TextField(max_length=300, blank=False)
    price = models.PositiveIntegerField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    tags = SortedManyToManyField(AdvertTag)
    author = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()

    class Meta:
        ordering = ["id"]


class AdvertImage(SafeDeleteModel):
    file = models.FileField(upload_to="img")
    author = models.CharField(max_length=100, blank=False)
    advert = models.ForeignKey(
        Advert, related_name="image", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["id"]


# soft deleting images of advert
@receiver(models.signals.pre_delete, sender=Advert)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for image in instance.image.iterator():
        image.delete()
