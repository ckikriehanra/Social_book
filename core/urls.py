"""Define URL for Social_book app"""

from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [ 
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
]