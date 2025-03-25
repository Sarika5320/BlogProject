from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Your password must be at least 8 characters long and cannot be entirely numeric."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def clean_password1(self):
    password = self.cleaned_data.get("password1")

    if not password:  # Prevents NoneType error
        raise ValidationError("Password is required.")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if password.isdigit():
        raise ValidationError("Password cannot be entirely numeric.")

    return password


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "profile_picture"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
