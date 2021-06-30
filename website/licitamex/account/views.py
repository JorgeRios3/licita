from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, ContactForm
from .models import Profile
import paypalrestsdk
import json
from paypalrestsdk.notifications import WebhookEvent
from django.views.generic import TemplateView



myapi = paypalrestsdk.Api({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


@require_POST
@csrf_exempt
def paypal_webhooks(request):
    transmission_id = request.headers['Paypal-Transmission-Id']
    timestamp = request.headers['Paypal-Transmission-Time']
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    event_body = request.body.decode('utf-8')
    cert_url = request.headers['Paypal-Cert-Url']
    auth_algo = request.headers['Paypal-Auth-Algo']
    actual_signature = request.headers['Paypal-Transmission-Sig']

    #response = WebhookEvent.verify(
    #    transmission_id, 
    #    timestamp, 
    #    webhook_id, 
    #    event_body, 
    #    cert_url, 
    #    actual_signature, 
    #    auth_algo
    #)

    #if response:
    if True:
        obj = json.loads(request.body)
        print(obj)

        event_type = obj.get('event_type')
        resource = obj.get('resource')

        if event_type == 'PAYMENT.SALE.COMPLETED':
            print(resource)
        elif event_type == 'PAYMENT.SALE.REFUNDED':
            print(resource)
        elif event_type == 'PAYMENT.SALE.REVERSED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.UPDATED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.EXPIRED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.SUSPENDED':
            print(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.PAYMENT.FAILED':
            print(resource)
        else:
            print("CATALOG UPDATE")

    return HttpResponse(status=200)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')

            if request.session.get('subscription_plan') == 'Basica':
                plan_id = settings.PAYPAL_PLAN_MONTHLY_ID
                data = {
                    'plan_id': plan_id,
                    "subscriber": {
                        "name": {
                          "given_name": user_form.data['first_name'],
                          "surname": user_form.data['last_name']
                        },
                        "email_address": user_form.data['email']
                    },
                    "custom_id": user_form.data['username'],
                    "application_context": {
                        "brand_name": "Licitamex",
                        "locale": "en-MX",
                        "shipping_preference": "NO_SHIPPING",
                        "user_action": "SUBSCRIBE_NOW",
                        "payment_method": {
                            "payer_selected": "PAYPAL",
                            "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                        },
                        "return_url": "https://www.consultalicitamex.com/account/register-done/",
                        "cancel_url": "https://www.consultalicitamex.com/account/register-done/"
                    }
                }
                ret = myapi.post("v1/billing/subscriptions", data)
                if ret['status'] == 'APPROVAL_PENDING':
                    # Create inactive user and profile

                    #new_user = user_form.save(commit=False)
                    #new_user.set_password(user_form.cleaned_data['password'])
                    #new_user.is_active = False
                    #new_user.save()
                    #Profile.objects.create(
                    #    user=new_user, subscription_id=ret['id'])

                    for link in ret['links']:
                        if link['rel'] == 'approve':
                            redirect_url = link['href']

                    return HttpResponseRedirect(redirect_url)

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
        else:
            messages.error(request, 'Error actualizando el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Contacto Licitamex"
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',
                          ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            # return redirect ('../../account/contact_message_done.html')
            return render(request, 'account/contact_message_done.html', {'form': form})

    form = ContactForm()
    return render(request, "account/contact.html", {'form': form})


class RegisterDonePageView(TemplateView):
    template_name = 'account/register_done.html'
