from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if  password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used.')
                return redirect('users:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used.')
                return redirect('users:signup')
            else:
                new_account = User.objects.create_user(username=username, 
                    email=email, password=password)
                new_account.save()
            
                #Make new profile for this user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, 
                    id_user=user_model.id)
                new_profile.save()
                #Log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('core:settings')
        else:
            messages.info('Password didn\'t match.')
            return redirect('users:signup')
    else:
        return render(request, 'users/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            #Signin and redirect
            auth.login(request, user)
            return redirect('core:index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('users:signin')

    else:
        return render(request, 'users/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('users:signin')

