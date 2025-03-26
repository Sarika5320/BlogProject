from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from .models import UserProfile 
from .forms import SignupForm
from admin_app.utils import send_notification_email


User = get_user_model()

# Register View
def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("accounts:login")  #Redirect after successful signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, "accounts/register.html", {"form": form})

# Custom Login View
def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_app:admin_dashboard")
            else:
                return redirect("user_app:home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

# Custom Logout View
def custom_logout(request):
    logout(request)
    return redirect("user_app:home")

# Password Reset Request View (Updated)
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = request.build_absolute_uri(
                reverse("accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            subject = "Password Reset Request"
            message = render_to_string("accounts/password_reset_email.html", {
                "reset_url": reset_url,
                "user": user
            })

            # ✅ Send using your reusable email function
            send_notification_email(subject, message, user.email)

            messages.success(request, "Password reset link sent to your email.")
            return redirect("accounts:password_reset_done")

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, "accounts/password_reset.html")

# Password Reset Confirm View
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.error(request, "Invalid or expired password reset link.")
            return redirect("accounts:password_reset_request")

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password successfully reset. You can now log in.")
                return redirect("accounts:login")
            else:
                messages.error(request, "Passwords do not match.")

        return render(request, "accounts/password_reset_confirm.html")

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("accounts:password_reset_request")

# Password Reset Done View
def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")
