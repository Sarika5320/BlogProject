from django.db import models
from django.contrib.auth.models import User
#BlogPost Model
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)  # Optional image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)  # Like feature

    def total_likes(self):
        return self.likes.count()  # Returns total likes
    
    def __str__(self):
        return self.title

#Comment Model
class Comment(models.Model):
    blog = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"