from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from mailjet_rest import Client
import os
from account.dynamo_functions import fetch_item
import json
from django.contrib.auth.models import User
from account.models import UsuarioFiltros, UsuarioLicitaciones
from fuzzywuzzy import fuzz
import datetime




class HomePageView(TemplateView):
    template_name = 'licitamex/index.html'


class TermsConditionsPageView(TemplateView):
    template_name = 'licitamex/terms-conditions.html'


class PrivacyPolicyPageView(TemplateView):
    template_name = 'licitamex/privacy-policy.html'

@csrf_exempt
def remove_licitacion(request):
	post_data = json.loads(request.body.decode("utf-8"))    
	licitacion_id = post_data.get("id", "")
	UsuarioLicitaciones.objects.filter(licitacion_id=licitacion_id).delete()
	return HttpResponse('deleted')


def validate_filtro(descripcion, filtro_val, filtro_precision ):
	if fuzz.partial_ratio(descripcion, filtro_val) > filtro_precision:
		if filtro_val in descripcion:
			return True
		else:
			return False
	return False
	
@csrf_exempt
def add_licitacion(request):
	post_data = json.loads(request.body.decode("utf-8"))    
	licitacion_id = post_data.get("id", "")
	licitacion = fetch_item("licitaciones", licitacion_id)
	filtros = UsuarioFiltros.objects.all()
	lista = []
	lista += list(filter(lambda x:validate_filtro(licitacion["descripcion"].lower(), x.grupo.lower(), 50), filtros))
	lista += list(filter(lambda x:validate_filtro(licitacion["descripcion"].lower(), x.familia.lower(), 50), filtros))
	lista += list(filter(lambda x:validate_filtro(licitacion["descripcion"].lower(), x.articulo.lower(), 50), filtros))
	filtrado = set(lista)
	print("viendo filtrado")
	print(filtrado)
	for x in filtrado:
		u = User.objects.filter(username= x.user)
		print("viendo esto")
		print(licitacion)
		nueva = add_licitacion_usuario(u[0], licitacion)
		nueva_licitacion_email(u[0].email, nueva)
	return HttpResponse('added')
	
def add_licitacion_usuario(usuario, licitacion):
	new_val = UsuarioLicitaciones()
	new_val.user = usuario
	new_val.licitacion_id = licitacion["id"]
	new_val.active = True
	new_val.expired = False
	new_val.expired_date = datetime.datetime.now().strftime("%Y-%m-%d")
	new_val.status = "Abierta"
	new_val.quotation = ""
	new_val.comments = {"comments":[]}
	new_val.description = licitacion["descripcion"]
	new_val.entidad = licitacion["entidad"]
	new_val.save()
	return new_val




def nueva_licitacion_email(email, licitacion):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Me"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": "Licitacion Agregada automaticamente",
			"HTMLPart": f"""<h3>La licitacion con id {licitacion.id}, descripcion: {licitacion.description}.</h3>
			<br/>Fue agregada automaticamente a tus licitaciones, esta accion se ejecuto de acuerdo a tus filtros configurados en el menu de configuracion.<br/>
			para ver la licitacion accede a tu portal <a href=\"https://consultalicitamex.com/\">consultalicitamex</a>"""
		}]
	}
	mailjet.send.create(data=data)

