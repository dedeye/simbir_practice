from django.db import models
from sortedm2m.fields import SortedManyToManyField


class AdvertTag(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name


class Advert(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=300, blank=True)
    contacts = models.TextField(max_length=200, blank=False)
    price = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)
    tags = SortedManyToManyField(AdvertTag,)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()
