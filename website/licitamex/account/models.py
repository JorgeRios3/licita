from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    subscription_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Perfil de usuario {self.user.username}'


class UsuarioLicitaciones(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    licitacion_id = models.CharField(max_length=100)
    active = models.BooleanField()
    expired = models.BooleanField()
    expired_date = models.DateField()
    status = models.CharField(max_length=100)
    quotation = models.CharField(max_length=300)
    comments = models.JSONField(default='{}')
    description = models.CharField(max_length=500)
    entidad = models.CharField(max_length=100)
    datos_comprador = models.JSONField(default='{}')

class CatalogoFiltros(models.Model):
    grupo = models.CharField(max_length=250, null=True)
    familia = models.CharField(max_length=250, null=True)
    articulo = models.CharField(max_length=250, null=True)

class UsuarioFiltros(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filtro_id = models.IntegerField()
    grupo = models.CharField(max_length=250, null=True)
    familia = models.CharField(max_length=250, null=True)
    articulo = models.CharField(max_length=250, null=True)
    activado = models.BooleanField(default=True)
