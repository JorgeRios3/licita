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
from .models import UsuarioFiltros, CatalogoFiltros
from django.core import serializers


def get_user_filtros(user_id):
    user = User.objects.get(pk=user_id)
    filtros = UsuarioFiltros.objects.filter(user=user)
    return filtros


def find_catalogo_filtro(grupo, familia, articulo):
    return CatalogoFiltros.objects.filter(familia=familia, grupo=grupo, articulo=articulo)


def add_filtro(request):
    post_data = json.loads(request.body.decode("utf-8"))
    grupo = post_data.get("grupo", '')
    familia = post_data.get("familia", '')
    articulo = post_data.get("articulo", '')
    user = User.objects.get(pk=request.user.id)
    catalogo_filtro = find_catalogo_filtro(grupo, familia, articulo)
    print("este es")
    print(catalogo_filtro)
    if not catalogo_filtro:
        catalogo_filtro = CatalogoFiltros()
        catalogo_filtro.grupo = grupo
        catalogo_filtro.familia = familia
        catalogo_filtro.articulo = articulo
        catalogo_filtro.save()
    else:
        catalogo_filtro=catalogo_filtro[0]
    usuario_filtro = UsuarioFiltros()
    usuario_filtro.user = user
    usuario_filtro.filtro_id = catalogo_filtro.pk
    usuario_filtro.grupo = catalogo_filtro.grupo 
    usuario_filtro.familia = catalogo_filtro.familia or ""
    usuario_filtro.articulo = catalogo_filtro.articulo or ""
    usuario_filtro.activado = True
    usuario_filtro.save()
    usuario_filtros = get_user_filtros(request.user.id)
    return render(request, 'account/configuracion.html', {"filtros":usuario_filtros})

def change_status_filtro(request):
    post_data = json.loads(request.body.decode("utf-8"))
    UsuarioFiltros.objects.filter(pk=post_data.get("id", 0)).update(activado= True if post_data.get("status", '') != "Desactivar" else False)
    usuario_filtros = get_user_filtros(request.user.id)
    return render(request, 'account/configuracion.html', {"filtros":usuario_filtros})

def filters(request):
    grupo = request.GET.get('grupo')
    familia = request.GET.get('familia')
    articulo = request.GET.get('articulo')
    filtros_litsta = []
    if grupo and not familia and not articulo:
        filtros = CatalogoFiltros.objects.filter(grupo__icontains=grupo)
        if not filtros:
            return JsonResponse([], safe=False)
        for x in filtros:
            filtros_litsta.append(x.grupo)
        set_values = set(filtros_litsta)
        lista = []
        for x in set_values:
            lista.append({"value":x, "text":x})
        return JsonResponse(lista, safe=False)
    if grupo and familia and not articulo:
        filtros = CatalogoFiltros.objects.filter(familia__icontains=familia, grupo__icontains=grupo)
        if not filtros:
            return JsonResponse([],
            safe=False)
        for x in filtros:
            filtros_litsta.append(x.familia)
        set_values = set(filtros_litsta)
        lista=[]
        for x in set_values:
            lista.append({"value":x, "text":x})
        return JsonResponse(lista, safe=False)
    if grupo and familia and articulo:
        filtros = CatalogoFiltros.objects.filter(familia__icontains=familia, grupo__icontains=grupo, articulo__icontains=articulo)
        if not filtros:
            return JsonResponse([],safe=False)
        print(filtros)
        lista=[]
        for x in filtros:
            lista.append({"value":x.articulo, "text":x.articulo, "id":x.id})
        return JsonResponse(lista, safe=False)



    
