from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from mailjet_rest import Client
import os



class HomePageView(TemplateView):
    template_name = 'licitamex/index.html'


class TermsConditionsPageView(TemplateView):
    template_name = 'licitamex/terms-conditions.html'


class PrivacyPolicyPageView(TemplateView):
    template_name = 'licitamex/privacy-policy.html'

@csrf_exempt
def add_licitacion(request):
    mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
    data = {
        'Messages': [
				{
						"From": {
								"Email": "norma.contreras@nilaconsulting.com.mx",
								"Name": "Me"
						},
						"To": [
								{
										"Email": "jorgecarlosriosb@gmail.com",
										"Name": "You"
								}
						],
						"Subject": "My first Mailjet Email!",
						"TextPart": "Greetings from Mailjet!",
						"HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
				}
		]
    
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return HttpResponse('Hello world')

