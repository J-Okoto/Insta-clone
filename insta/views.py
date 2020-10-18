from django.shortcuts import render,redirect
from .models import Profile,Image,Comment
from django.contrib.auth.decorators import login_required
from django.http  import Http404
import datetime as dt

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
    

@login_required(login_url='/accounts/login/')
def profile(request):
    title = 'Profile'
    
    return render(request, 'profile/profile.html')

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'name' in request.GET and request.GET["name"]: 
        search_name = request.GET.get("name")
        found_users = Profile.find_profile(search_name)
        message =f"{search_name}" 

        return render(request,'all-grams/search_results.html',{"message":message,"found_users":found_users})
    else:
        message = "Please enter a valid username"
    return render(request,'all-grams/search_results.html',{"message":message})