from django.db import models

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

    def __str__(self):
        return self.Event_Name
    

class Participant(models.Model):
    Participant_Name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.Participant_Name





