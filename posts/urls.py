from django.urls import path, include
from . import views

"""Define URL for posts app"""
app_name = 'posts'

urlpatterns = [ 
    path('upload', views.upload, name='upload'),
    path('like_post/<str:post_id>', views.like_post, name='like_post'),
    path('delete_post/<str:post_id>', views.delete_post, name='delete_post'),
]
