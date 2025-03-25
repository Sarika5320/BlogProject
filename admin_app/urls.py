app_name = 'admin_app' 
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-posts/', views.manage_posts, name='manage_posts'),

    path('manage-users/', views.manage_users, name='manage_users'), 
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('delete-post/<int:blog_id>/', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('manage-comments/', views.manage_comments, name='manage_comments'),
    path("delete-post/<int:blog_id>/", views.delete_post, name="delete_post"),


]