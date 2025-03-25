from django.urls import path
from . import views

app_name = "user_app"

urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("settings/", views.update_profile, name="settings"), 
    path("update-profile/", views.update_profile, name="update_profile"),
    path("create-blog/", views.create_blog, name="create_blog"),
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("blog/<int:blog_id>/edit/", views.edit_blog, name="edit_blog"),
    path("blog/<int:blog_id>/delete/", views.delete_blog, name="delete_blog"),
    path('like/<int:blog_id>/', views.like_post, name='like_post'), 
]