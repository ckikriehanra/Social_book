from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import FollowCount, Profile
from django.contrib.auth.models import User
from posts.views import Post
from users.views import Profile
from django.urls import reverse
import random


from posts.models import Post
# Create your views here.

@login_required
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    #Get all post of user who current user following
    followings = FollowCount.objects.filter(follower=request.user.username)
    posts = []
    for following in followings:
        for temp in Post.objects.filter(user=following.user):
            posts.append(temp)
    
    #Get all user who cureent user are is following.
    all_uers = User.objects.all()
    users_not_followings = []
    for temp in all_uers:
        if FollowCount.objects.filter(follower=request.user.username, 
            user=temp.username) or temp.username == request.user.username:
            #Followed
            pass
        else:
            #Not Follow, add to list to suggestion
            users_not_followings.append(temp)

        #Only get random 5 users to suggest
    random.shuffle(users_not_followings)
    profile_users_not_following_list = []
    if len(users_not_followings) > 5:
        users_not_followings = users_not_followings[:5]

    for temp in users_not_followings:
        profile_users_not_following = Profile.objects.filter(user=temp).first()
        if profile_users_not_following:
            profile_users_not_following_list.append(profile_users_not_following)
    
    context = { 
        'user_profile': user_profile,
        'posts': posts,
        'profile_users_not_following_list': profile_users_not_following_list,
    }
    
    return render(request, 'core/index.html', context)

@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    if request.method == 'POST':
        bio = request.POST['bio']
        location = request.POST['location']
        profileimg = request.FILES.get('image')
        #Process Profileimg
        if profileimg == None:
            #Use default image
            profileimg = user_profile.profileimg
        
        user_profile.profileimg = profileimg
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        context = {'user_profile': user_profile}
        return render(request, 'core/setting.html', context)
    else:
        return render(request, 'core/setting.html', context)

@login_required
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    posts = Post.objects.filter(user=user_object.username)
    len_posts = len(posts)

    #Compute no_followers and no_followings
    followers = FollowCount.objects.filter(user=pk)
    followings = FollowCount.objects.filter(follower=pk)
    len_followings = len_followers = 0
    if followers.first() != None:
        len_followers = len(followers)
    if followings.first() != None:
        len_followings = len(followings)
    
    #Check Follow or unfollow
    follower = request.user.username
    user = pk

    if FollowCount.objects.filter(follower=follower, user=user):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'user_object': user_object,
        'profile_object': profile_object,
        'posts': posts,
        'len_posts': len_posts,
        'len_followers': len_followers,
        'len_followings': len_followings,
        'button_text': button_text,
    }
    return render(request, 'core/profile.html', context)

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowCount.objects.filter(follower=follower, user=user).first():
            #Unfollow
            delete_follower = FollowCount.objects.filter(follower=follower, user=user).first()
            delete_follower.delete()
        else:
            #follow
            new_follower = FollowCount.objects.create(follower=follower, user=user)
            new_follower.save()
        return redirect(reverse('core:profile', kwargs={'pk':user}))

    return redirect('core:index')

@login_required
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        #Get all profile of needed users
        user_objects = User.objects.filter(username__icontains = username)
        profile_objects_list = []

        for temp in user_objects:
            profile_object = Profile.objects.filter(user=temp).first()
            if profile_object:
                profile_objects_list.append(profile_object)
    
    context = { 
        'user_profile': user_profile,
        'profile_objects_list': profile_objects_list,
        'len_profile_objects_list': len(profile_objects_list),
        'username': username
    }
    return render(request, 'core/search.html', context)