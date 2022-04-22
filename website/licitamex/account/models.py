from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    admin_user = models.IntegerField(default=0)
    company = models.CharField(max_length=50, blank=True, null=True)
    payment_vendor = models.CharField(max_length=50, blank=True, null=True)
    plan_is_active = models.BooleanField(default=False)
    users = models.JSONField(default='{}')
    status = models.CharField(max_length=50, blank=True, null=True)
    subscription_type =models.CharField(max_length=50, blank=True, null=True)
    subscription_id = models.CharField(max_length=200, blank=True, null=True)


class CustomUser(AbstractUser):
    reset_passowrd_hash = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Permiso(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    permiso = models.CharField(max_length=50, blank=True, null=True)


class UsuarioPermisos(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)


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

class GrupoFiltros(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    filtro_id = models.IntegerField()
    grupo = models.CharField(max_length=250, default="")
    familia = models.CharField(max_length=250, default="", null=True)
    articulo = models.CharField(max_length=250, default="", null=True)
    activado = models.BooleanField(default=True)
