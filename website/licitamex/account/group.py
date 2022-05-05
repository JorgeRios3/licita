from django.http import HttpResponse
from .models import Group, UsuarioLicitaciones
import json
import datetime
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.core import serializers
from .models import CustomUser, UsuarioPermisos, Permiso
from .forms import NewUserForm
from .utils import make_url, group_users
import re
from .filtros import get_user_filtros
from .mails import invitacion_usuario_email



def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
       return True
    else:
        False





def add_user(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        print(user_form)
        users = CustomUser.objects.filter(email = user_form.data['email'])
        print(users)
        errors =[]
        if not check_email(user_form.data['email']):
            errors.append("el email no es una direccion de correco valida")
        if users:
            errors.append("el correo que intentas usar ya existe")

        if users or errors:
            filtros = get_user_filtros(request.user.id)
            usuarios = group_users(request.user.id)
            return render(request, 'account/configuracion.html', {"filtros":filtros, "usuarios":usuarios, "form":user_form, "errors":errors})
        else:
            rule_user = CustomUser.objects.get(pk=request.user.id)
            user = CustomUser()
            user.username =user_form.data['username']
            user.first_name = user_form.data['first_name']
            user.last_name = user_form.data['last_name']
            user.email = user_form.data['email']
            user.set_password(user_form.data['password'])
            user.group = rule_user.group
            user.save()
            permiso = Permiso.objects.get(pk=2) 
            up = UsuarioPermisos(usuario=user, permiso=permiso, group=user.group)
            up.save()
            invitacion_usuario_email(user.email, rule_user.group.company)
            return HttpResponseRedirect(make_url("account/configuracion"))