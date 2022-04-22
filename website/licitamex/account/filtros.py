from django.http import HttpResponse
from .models import Group, UsuarioLicitaciones
import json
import datetime
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.http import JsonResponse
from .models import CatalogoFiltros, GrupoFiltros
from django.core import serializers
from .models import CustomUser, Group,Permiso,UsuarioPermisos
from .configuracion_data import data_configuracion
from django.views.decorators.cache import never_cache



def get_user_filtros(user_id):
    user = CustomUser.objects.get(pk=user_id)
    filtros = GrupoFiltros.objects.filter(group=user.group.id)
    return filtros


def find_catalogo_filtro(grupo, familia, articulo):
    return CatalogoFiltros.objects.filter(familia=familia, grupo=grupo, articulo=articulo)


def add_filtro(request):
    post_data = json.loads(request.body.decode("utf-8"))
    grupo = post_data.get("grupo", '')
    familia = post_data.get("familia", '')
    articulo = post_data.get("articulo", '')
    user = CustomUser.objects.get(pk=request.user.id)
    catalogo_filtro = find_catalogo_filtro(grupo, familia, articulo)
    print("este es")
    print(catalogo_filtro)
    print(user.group)
    if not catalogo_filtro:
        catalogo_filtro = CatalogoFiltros()
        catalogo_filtro.grupo = grupo
        catalogo_filtro.familia = familia
        catalogo_filtro.articulo = articulo
        catalogo_filtro.save()
    else:
        catalogo_filtro=catalogo_filtro[0]
    grupo_filtro = GrupoFiltros()
    grupo_filtro.group = user.group
    grupo_filtro.filtro_id = catalogo_filtro.pk
    grupo_filtro.grupo = catalogo_filtro.grupo
    grupo_filtro.familia = catalogo_filtro.familia or ""
    grupo_filtro.articulo = catalogo_filtro.articulo or ""
    grupo_filtro.activado = True
    grupo_filtro.save()
    usuario_filtros = get_user_filtros(request.user.id)

    return render(request, 'account/configuracion.html', {"filtros":usuario_filtros})

@never_cache
def delete_user_permision(request):
    post_data = json.loads(request.body.decode("utf-8"))
    print("viendo el data  ", post_data)
    up = UsuarioPermisos.objects.get(pk=post_data["permiso_id"])
    up.delete()
    data = data_configuracion(request)
    return render(request, 'account/configuracion.html', {"filtros":data["filtros"], 
    "form":data["form"], "usuarios":data["usuarios"], "group":data["group"], 
    "is_admin":data["is_admin"], "permisos_usuarios":data["permisos_usuarios"], "permisos":data["permisos"]})

@never_cache
def add_user_permision(request):
    post_data = json.loads(request.body.decode("utf-8"))
    print("viendo el data  ", post_data)
    cu = CustomUser.objects.filter(pk=int(post_data["usuario_id"]))
    print("viendo el cu ", cu)
    permiso = Permiso.objects.filter(pk=int(post_data["permiso_id"]))
    up = UsuarioPermisos(usuario=cu[0], permiso=permiso[0], group=cu[0].group)
    up.save()
    data = data_configuracion(request)
    return render(request, 'account/configuracion.html', {"filtros":data["filtros"], 
    "form":data["form"], "usuarios":data["usuarios"], "group":data["group"], 
    "is_admin":data["is_admin"], "permisos_usuarios":data["permisos_usuarios"], "permisos":data["permisos"]})

def delete_group_user(request):
    post_data = json.loads(request.body.decode("utf-8"))
    cu = CustomUser.objects.filter(pk=post_data.get("id", 0))
    group = cu[0].group
    cu.delete()
    data = data_configuracion(request)
    return render(request, 'account/configuracion.html', {"filtros":data["filtros"], 
    "form":data["form"], "usuarios":data["usuarios"], "group":data["group"], 
    "is_admin":data["is_admin"], "permisos_usuarios":data["permisos_usuarios"], "permisos":data["permisos"]})



def change_status_filtro(request):
    post_data = json.loads(request.body.decode("utf-8"))
    GrupoFiltros.objects.filter(pk=post_data.get("id", 0)).update(activado= True if post_data.get("status", '') != "Desactivar" else False)
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



    
