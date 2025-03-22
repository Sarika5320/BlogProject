from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile


# Function to allow only superusers (admins)
def superuser_required(user):
    return user.is_superuser

# Admin Dashboard View (Only accessible to superusers)
@user_passes_test(superuser_required)
@login_required
def admin_dashboard(request):
    return render(request, 'admin_app/dashboard.html')

# Manage Blog Posts View
@user_passes_test(superuser_required)
@login_required
def manage_posts(request):
    return render(request, 'admin_app/manage_posts.html')


#--------------------------------------------------------------------#
#user management

@login_required
def manage_users(request):
    if not request.user.is_staff:  
        return redirect("home")

    users = UserProfile.objects.select_related('user').all()
    return render(request, "admin_app/manage_users.html", {"users": users})

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
    messages.success(request, "User deleted successfully.")
    return redirect("admin_app:manage_users")
