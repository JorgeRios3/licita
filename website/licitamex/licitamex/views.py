from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

class HomePageView(TemplateView):
    template_name = 'licitamex/index.html'


class TermsConditionsPageView(TemplateView):
    template_name = 'licitamex/terms-conditions.html'


class PrivacyPolicyPageView(TemplateView):
    template_name = 'licitamex/privacy-policy.html'
