from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    Category_Name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Category_Name

class Event(models.Model):
    Event_Name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    Date_and_Time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="cat",
    )
    asset = models.ImageField(upload_to='event_asset', blank=True, null=True, default='event_asset/default-img.jpg')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_event')

    def __str__(self):
        return self.Event_Name
    






