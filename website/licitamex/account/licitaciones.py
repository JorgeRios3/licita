from django.http import HttpResponse
from .models import UsuarioLicitaciones
import json
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .dynamo_functions import fetch_items_table
from django.template.response import TemplateResponse
from django.http import JsonResponse
from .dynamo_functions import fetch_items_table
from .utils import compare_user
from django.core import serializers



def licitacion(request, id):
    print("viendo el id", id)
    licitacion = UsuarioLicitaciones.objects.filter(pk=id)
    serialized_obj = serializers.serialize('json', licitacion)
    ob_json = json.loads(serialized_obj)
    return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})


def search_licitacion_by_name(request):
    nombre = request.GET.get('nombre')
    print("viendo nombre ", nombre)
    items = fetch_items_table("licitaciones", nombre)["Items"]
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items, "items_qty":len(validated_items)})

def compare_user(licitacion, user_licitaciones):
    val = list(filter(lambda x: x.licitacion_id==licitacion.get("id"), user_licitaciones))
    if val:
        licitacion["selected"]=True
    else:
        licitacion["selected"]=False
    return licitacion


def get_user_licitaciones(user_id):
    user = User.objects.get(pk=user_id)
    licitaciones = UsuarioLicitaciones.objects.filter(user=user)
    return licitaciones

def change_status(request):
    post_data = json.loads(request.body.decode("utf-8"))
    UsuarioLicitaciones.objects.filter(pk=post_data.get("id", 0)).update(status=post_data.get("status", ''))
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})

    
def add_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    user = User.objects.get(pk=request.user.id)
    licitacion = UsuarioLicitaciones()
    licitacion.user = user
    licitacion.licitacion_id = post_data.get("valor", 0)
    licitacion.active = True
    licitacion.expired = False
    licitacion.expired_date = datetime.datetime.now().strftime("%Y-%m-%d")
    licitacion.status = "Abierta"
    licitacion.quotation = "aqui va el documento de la cotizacion del usuario"
    licitacion.comments = "aqui van los comentarios de como va el avance de la licitacion"
    licitacion.description = post_data.get("description", "")
    licitacion.entidad = post_data.get("entidad", "")
    licitacion.save()
    items = fetch_items_table("licitaciones")["Items"]
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items})
 
def remove_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    licitacion =UsuarioLicitaciones.objects.filter(id=post_data.get("valor", 0))
    licitacion.delete()
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})
    
