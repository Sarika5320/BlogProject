from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')  # Customize admin panel
    search_fields = ('user__username', 'phone')  # Enable search

admin.site.register(UserProfile, UserProfileAdmin)
