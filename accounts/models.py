from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="profile_pics/default.jpg")
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    