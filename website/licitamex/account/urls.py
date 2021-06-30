from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    #POST views
    path('paypal-webhooks', csrf_exempt(views.paypal_webhooks), name='paypal_webhooks'),
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('contact/', views.contact, name='contact'),
    path('register-done/', views.RegisterDonePageView.as_view(), name='register_done'),
    
    #path('process_subscription/', views.process_subscription, name='process_subscription'),
]
