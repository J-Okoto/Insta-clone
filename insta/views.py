import os
from django.shortcuts import render,redirect
from .models import Profile,Image,Comment,Like,Follow
from django.contrib.auth.decorators import login_required
from django.http  import Http404
import datetime as dt
from . forms import ImageForm, CommentForm, ProfileUpdateForm,UpdateImageCaption 
from django.contrib.auth.models import User

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')
    

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

@login_required(login_url='/accounts/login/')
def single_user(request,id):
    try:
        user = Profile.objects.get(id=id)
    except:
        raise Http404()
    return render(request,'all-grams/single.html',{"user":user})

@login_required(login_url='/accounts/login/')
def single_image(request,image_id): 
    try:
        image = Image.objects.get(id= image_id)
    except:
        raise Http404()
    return render(request, 'all-grams/single_image.html',{"image":image})

def post(request):
    '''
    View function that displays a forms that allows users to upload images
    '''
    current_user = request.user

    if request.method == 'POST':

        form = ImageForm(request.POST ,request.FILES)

        if form.is_valid():
            image = form.save(commit = False)
            image.user_key = current_user
            image.likes +=0
            image.save() 
        return redirect( timeline)
            
    else:
        form = ImageForm() 
    return render(request, 'all-grams/post.html',{"form" : form}) 

@login_required(login_url='/accounts/login/')

def timeline(request):
    date = dt.date.today()
    current_user = request.user 
    
    images1 =[]
    

    post = Image.objects.all()
    for item in post:
            images1.append(item)
            images= list(reversed(images1))                                                                                                                                                                                                                                                                                                                                                                  
    return render(request, 'all-grams/timeline.html',{"date":date,"timeline_images":images})

@login_required(login_url='/accounts/login/')
def profile(request):
    title = 'Profile'
    current_user = request.user
    try:
        profile = Profile.objects.get(user_id = current_user)
        following = Follow.objects.filter(follower = current_user)
        followers = Follow.objects.filter(user = profile) 
    except:
        profile = Profile.objects.get(username = 'default_user')
        following = Follow.objects.filter(follower = current_user)
        followers = Follow.objects.filter(user = profile)

    return render(request, 'profile/profile.html',{"profile":profile,"current_user":current_user,"following":following,"followers":followers})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user 
    title = 'Update Profile'
    try:
        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.profile_photo = form.cleaned_data['profile_photo']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.username = form.cleaned_data['username']
                requested_profile.save_profile()
                return redirect( profile )
        else:
            form = ProfileUpdateForm()
    except:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                new_profile = Profile(profile_photo= form.cleaned_data['profile_photo'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'],user = current_user)
                new_profile.save_profile()
                return redirect( profile )
        else:
            form = ProfileUpdateForm()


    return render(request,'profile/update_profile.html',{"title":title,"current_user":current_user,"form":form})


@login_required(login_url='/accounts/login/')
def view_profiles(request):
    all_profiles = Profile.objects.all()
    return render(request,'profile/all.html',{"all_profiles":all_profiles}) 

@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    comments = Comment.objects.filter(image_id=image_id)
    current_image = Image.objects.get(id=image_id)
    current_user = request.user

    if request.method == 'POST':

        form = CommentForm(request.POST)
        logger_in = request.user
        

        if form.is_valid():
            comment = form.save(commit = False)
            comment.user_id= current_user
            comment.image_id = current_image
            current_image.comments_number+=1
            current_image.save_image()
            comment.save()

            return redirect(timeline)
    else:
        form = CommentForm()
    return render(request,'all-grams/comment.html',{"form":form,"comments":comments})  
