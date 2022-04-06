from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from . import group
urlpatterns = [
    #POST views
    path('add_user', group.add_user, name='add_user'),


    
    #path('process_subscription/', views.process_subscription, name='process_subscription'),
]
