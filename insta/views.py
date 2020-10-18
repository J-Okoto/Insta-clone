from django.shortcuts import render,redirect
from .models import Profile,Image,Comment,Like,Follow
from django.contrib.auth.decorators import login_required
from django.http  import Http404
import datetime as dt
from . forms import ImageForm, CommentForm, ProfileUpdateForm,UpdateImageCaption 

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

            
    else:
        form = ImageForm() 
    return render(request, 'all-grams/post.html',{"form" : form}) 

@login_required(login_url='/accounts/login/')
def timeline(request):
    date = dt.date.today()
    current_user = request.user 
    followed_people= []
    images1 =[]
    following  = Follow.objects.filter(follower = current_user)
    is_following = Follow.objects.filter(follower = current_user).count()
    try:
        if is_following != 0:
            for following_object in following:
                image_set = Profile.objects.filter(id = following_object.user.id)
                for item in image_set:
                    followed_people.append(item)
            for followed_profile in followed_people:
                post = Image.objects.filter(user_key = followed_profile.user)
                for item in post:
                    images1.append(item)
                    images= list(reversed(images1))                                                                                                                                                                                                                                                                                                                                                                  
            return render(request, 'all-grams/timeline.html',{"date":date,"timeline_images":images})
    except:
        raise Http404
    return render(request, 'profile/profile.html') 

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
