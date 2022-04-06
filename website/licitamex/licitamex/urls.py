"""licitamex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('account/', include('account.urls')),
    path('group/', include('account.group_urls')),
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='index'),
    path('terms-conditions/', views.TermsConditionsPageView.as_view(), name='terms-conditions'),
    path('privacy-policy/', views.PrivacyPolicyPageView.as_view(), name='privacy-policy'),
    path('add_licitacion', views.add_licitacion, name='add-licitacion'),
    path('remove_licitacion', views.remove_licitacion, name='remove-licitacion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
