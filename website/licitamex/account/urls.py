from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views
from . import licitaciones
from . import filtros

urlpatterns = [
    #POST views
    path('paypal-webhooks', csrf_exempt(views.paypal_webhooks), name='paypal_webhooks'),
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('configuracion', views.configuracion, name='configuracion'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('contact/', views.contact, name='contact'),
    path('register-done/', views.RegisterDonePageView.as_view(), name='register_done'),
    path('my_login/', views.my_login, name='my_login'),
    path('licitaciones/', views.licitaciones, name='licitaciones'),
    path('licitacion/<id>', licitaciones.licitacion, name='licitacion'),
    path('add_licitacion', licitaciones.add_licitacion, name='add_licitacion'),
    path('change_status_licitacion', licitaciones.change_status, name="change_status"),
    path('remove_licitacion', licitaciones.remove_licitacion, name='remove_licitacion'),
    path('search_licitacion_by_name', licitaciones.search_licitacion_by_name, name='search_licitacion_by_name'),
    path('filter', filtros.filters, name='filters'),
    path('add_filtro', filtros.add_filtro, name='add_filtro'),
    path('change_status_filtro', filtros.change_status_filtro, name="change_status_filtro"),


    
    #path('process_subscription/', views.process_subscription, name='process_subscription'),
]
