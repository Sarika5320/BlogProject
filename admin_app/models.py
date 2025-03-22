from django.db import models

# Create your models here.

class HeroVideo(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='hero_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title