from .models import UsuarioLicitaciones
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
import json
from django.core import serializers

def get_user_licitaciones(user_id):
    user = User.objects.get(pk=user_id)
    licitaciones = UsuarioLicitaciones.objects.filter(user=user)
    return licitaciones

def change_status(request):
    post_data = json.loads(request.body.decode("utf-8"))
    UsuarioLicitaciones.objects.filter(pk=post_data.get("id", 0)).update(status=post_data.get("status", ''))
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})


def licitacion(request, id):
    print("viendo el id", id)
    licitacion = UsuarioLicitaciones.objects.filter(pk=id)
    serialized_obj = serializers.serialize('json', licitacion)
    ob_json = json.loads(serialized_obj)
    return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})


def delete_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    licitacion = UsuarioLicitaciones.objects.filter(pk=post_data.get("id", 0))
    licitacion = licitacion[0]
    licitacion.delete()
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})


