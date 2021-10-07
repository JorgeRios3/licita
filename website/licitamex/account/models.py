from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    reset_passowrd_hash = models.CharField(max_length=100, null=True)


class Group(models.Model):
    admin_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    subscription_id = models.CharField(max_length=50, blank=True, null=True)
    plan_active = models.BooleanField(default=False)


class UserPlan(models.Model):
    owner_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, blank=True, null=True)
    plan_active = models.BooleanField(default=False)
    status = models.CharField(max_length=50, blank=True, null=True)
    users = models.JSONField(default='{}')


class UsuarioLicitaciones(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    licitacion_id = models.CharField(max_length=100)
    active = models.BooleanField()
    expired = models.BooleanField()
    expired_date = models.DateField()
    status = models.CharField(max_length=100)
    quotation = models.TextField()
    comments = models.JSONField(default='{}')
    description = models.CharField(max_length=500)
    entidad = models.CharField(max_length=100)
    datos_comprador = models.JSONField(default='{}')

class CatalogoFiltros(models.Model):
    grupo = models.CharField(max_length=250, null=True)
    familia = models.CharField(max_length=250, null=True)
    articulo = models.CharField(max_length=250, null=True)

class UsuarioFiltros(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    filtro_id = models.IntegerField()
    grupo = models.CharField(max_length=250, default="")
    familia = models.CharField(max_length=250, default="", null=True)
    articulo = models.CharField(max_length=250, default="", null=True)
    activado = models.BooleanField(default=True)
