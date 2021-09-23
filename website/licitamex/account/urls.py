from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views
from . import licitaciones
from . import filtros
from . import mis_licitaciones

urlpatterns = [
    #POST views
    path('paypal-webhooks', csrf_exempt(views.paypal_webhooks), name='paypal_webhooks'),
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('configuracion', views.configuracion, name='configuracion'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('contact/', views.contact, name='contact'),
    path('cancel/', views.cancel, name='cancel'),
    path('register-done/', views.RegisterDonePageView.as_view(), name='register_done2'),
    re_path(r'^register-done/$', views.RegisterDone, name='register_done'),
    path('my_login/', views.my_login, name='my_login'),
    path('licitaciones/', views.licitaciones, name='licitaciones'),
    path('activate_licitacion', licitaciones.activate_licitacion, name='activate_licitacion'),
    path('search_licitacion_by_name', licitaciones.search_licitacion_by_name, name='search_licitacion_by_name'),
    path('search_mi_portallicitacion_by_name', licitaciones.search_mi_portallicitacion_by_name, name='search_mi_portallicitacion_by_name'),
    path('search_filtro_by_name', licitaciones.search_filtro_by_name, name='search_filtro_by_name'),
    path('inactive_licitacion', licitaciones.inactive_licitacion, name='inactive_licitacion'),
    path('filter', filtros.filters, name='filters'),
    path('add_filtro', filtros.add_filtro, name='add_filtro'),
    path('change_status_filtro', filtros.change_status_filtro, name="change_status_filtro"),
    path('licitacion/<id>', mis_licitaciones.licitacion, name='licitacion'),
    path('delete_licitacion', mis_licitaciones.delete_licitacion, name='delete_licitacion'),
    path('change_status_licitacion', mis_licitaciones.change_status, name="change_status"),
    path('add_cotizacion/<id>', mis_licitaciones.add_cotizacion, name='add_cotizacion')

    
    #path('process_subscription/', views.process_subscription, name='process_subscription'),
]
