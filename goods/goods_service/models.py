import os

from django.db import models
from django.dispatch import receiver

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
