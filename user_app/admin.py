from django.contrib import admin
from .models import BlogPost, Comment
from accounts.models import UserProfile

# Blog Post Admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)

# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "content", "created_at")
    search_fields = ("user__username", "blog__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
