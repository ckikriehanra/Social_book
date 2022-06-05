from django.urls import path
from . import views

"""Define URL for users app"""

app_name = 'users'

urlpatterns = [ 
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]