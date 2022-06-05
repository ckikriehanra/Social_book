from django.contrib import admin
from .models import Profile, FollowCount

# Register your models here.
admin.site.register(Profile)
admin.site.register(FollowCount)