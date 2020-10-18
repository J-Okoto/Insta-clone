from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    title = 'Profile'
    
    return render(request, 'profile/profile.html')