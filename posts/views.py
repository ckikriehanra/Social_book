from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, LikePost

# Create your views here.
@login_required
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        if image == None or caption == '':
            messages.info(request,"You must upload image and write caption before submit.")
        else:
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
        return redirect('core:index')
    else:
        return redirect('core:index')

def like_post(request, post_id):
    username= request.user.username
    post = Post.objects.get(id=post_id)

    #Check like or unlike 
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        #Like
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
    else:
        #Dislike
        post.no_of_likes = post.no_of_likes - 1
        like_filter.delete()
        post.save()
    return redirect('core:index')

def delete_post(request, post_id):
    post_delete = Post.objects.get(id=post_id)
    post_delete.delete()

    return redirect('core:index')
