from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile
from django.db.models import Q
from django.core.paginator import Paginator
from user_app.models import BlogPost
from user_app.models import Comment

# Ensure only admins can delete posts
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Function to allow only superusers (admins)
def superuser_required(user):
    return user.is_superuser

# Admin Dashboard View (Only accessible to superusers)
@user_passes_test(is_admin)
def admin_dashboard(request):
    user_count = User.objects.count()
    post_count = BlogPost.objects.count()
    comment_count = Comment.objects.count()
    posts = BlogPost.objects.all().order_by('-created_at')[:5]  # Show latest 5 posts
    comments = Comment.objects.all().order_by('-created_at')[:5]  # Show latest 5 comments

    return render(request, 'admin_app/dashboard.html', {
        'user_count': user_count,
        'post_count': post_count,
        'comment_count': comment_count,
        'posts': posts,
        'comments': comments
    })

# Manage Blog Posts View
@user_passes_test(superuser_required)
@user_passes_test(is_admin)
def manage_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'admin_app/manage_posts.html', {'posts': posts})


#--------------------------------------------------------------------#
#user management

def manage_users(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')

    users = User.objects.all()

    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    # Apply role filter
    if role_filter:
        users = users.filter(is_staff=True if role_filter == 'admin' else False)

    # Apply active/inactive filter
    if status_filter:
        users = users.filter(is_active=True if status_filter == 'active' else False)

    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_app/manage_users.html', {'page_obj': page_obj, 'search_query': search_query})


@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return redirect("home")

    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect("admin_app:manage_users")

    return render(request, "admin_app/edit_user.html", {"user": user})

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect("home")

    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("admin_app:manage_users")

# Delete Post View 
@user_passes_test(is_admin)
def delete_post(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    blog.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('admin_app:manage_posts')  # Redirect to admin post list

# Delete Comment View 
@user_passes_test(is_admin)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('admin_app:manage_comments')



@user_passes_test(is_admin)
def manage_comments(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'admin_app/manage_comments.html', {'comments': comments})