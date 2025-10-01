from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile/default.png')
    phone_number = models.CharField(blank=True, max_length=15)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

