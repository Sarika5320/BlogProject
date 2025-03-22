from django.shortcuts import render
from admin_app.models import HeroVideo

# Create your views here.

def home(request):
    videos = HeroVideo.objects.all()  # Fetch all hero videos
    return render(request, 'user_app/home.html', {'videos': videos}) # Loads home.html from templates/user_app/