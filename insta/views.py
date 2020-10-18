from django.shortcuts import render
from .models import Profile

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def profile(request):
    title = 'Profile'
    
    return render(request, 'profile/profile.html')