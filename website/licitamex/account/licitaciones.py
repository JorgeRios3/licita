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
from .utils import compare_user
from django.core import serializers
from .mis_licitaciones import get_user_licitaciones, licitacion
from .filtros import get_user_filtros

from fuzzywuzzy import fuzz



def search_licitacion_by_name(request):
    nombre = request.GET.get('nombre')
    dependencia = request.GET.get('dependencia')
    items = fetch_items_table("licitaciones", nombre)["Items"]
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    if dependencia:
        validated_items = list(filter(lambda x: x["entidad"] == dependencia, validated_items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items, "items_qty":len(validated_items)})

def search_filtro_by_name(request):
    usuario_filtros = get_user_filtros(request.user.id)
    nombre = request.GET.get('nombre')
    if nombre.strip():
        grupo = list(filter(lambda x:fuzz.partial_ratio(nombre.lower(), x.grupo.lower()) > 70, usuario_filtros))
        familia = list(filter(lambda x:fuzz.partial_ratio(nombre.lower(), x.familia.lower()) > 70, usuario_filtros))
        articulo = list(filter(lambda x:fuzz.partial_ratio(nombre.lower(), x.articulo.lower()) > 70, usuario_filtros))
        searched_items = grupo+familia+articulo
    else:
        searched_items = usuario_filtros
    return render(request, 'account/configuracion.html', {"filtros":searched_items})

def search_mi_portallicitacion_by_name(request):
    nombre = request.GET.get('nombre')
    user = User.objects.get(pk=request.user.id)
    licitaciones = UsuarioLicitaciones.objects.filter(user=user)
    if nombre.strip():
        searched_items = list(filter(lambda x:fuzz.partial_ratio(nombre.lower(), x.description.lower()) > 70, licitaciones))
    else:
        searched_items = licitaciones
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', "licitaciones":searched_items})


def compare_user(licitacion, user_licitaciones):    
    val = list(filter(lambda x: x.licitacion_id==licitacion.get("id"), user_licitaciones))
    if val:
        licitacion["selected"]=True
    else:
        licitacion["selected"]=False
    return licitacion


    
def activate_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    user = User.objects.get(pk=request.user.id)
    licitacion = UsuarioLicitaciones()
    licitacion.user = user
    licitacion.licitacion_id = post_data.get("valor", 0)
    licitacion.active = True
    licitacion.expired = False
    licitacion.expired_date = datetime.datetime.now().strftime("%Y-%m-%d")
    licitacion.status = "Abierta"
    licitacion.quotation = ""
    licitacion.comments = {"comments":[]}
    licitacion.description = post_data.get("description", "")
    licitacion.entidad = post_data.get("entidad", "")
    licitacion.save()
    items = fetch_items_table("licitaciones")["Items"]
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items})
 
def inactive_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    print("viendo el id", post_data.get("valor", 0))
    licitacion = UsuarioLicitaciones.objects.filter(licitacion_id=post_data.get("valor", 0))
    print("viendo licitacion ", licitacion)
    licitacion=licitacion[0]
    licitacion.delete()
    items = fetch_items_table("licitaciones")["Items"]
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items})
    
