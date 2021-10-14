from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, ContactForm, ChangePasswordForm
from .models import UsuarioLicitaciones, UserPlan, CustomUser
from django.contrib.auth.models import User
import paypalrestsdk
import json
from paypalrestsdk.notifications import WebhookEvent
from .dynamo_functions import fetch_items_table, fetch_dependencias
from .licitaciones import get_user_licitaciones
from .filtros import get_user_filtros
from .utils import compare_user
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
import stripe
from django.views.generic import TemplateView
from mailjet_rest import Client
from datetime import datetime
from datetime import timedelta
from django.urls import reverse





myapi = paypalrestsdk.Api({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        date =datetime.now() + timedelta(days=1)
        date=date.utcnow().timestamp(),
        user = CustomUser.objects.filter(email=email)
        hash = f"{date}"
        hash = hash.replace("(", "").replace(")", "").replace(",", "")
        user = user[0]
        user.reset_passowrd_hash = hash
        user.save()
        reset_password_email(email, hash)
        return render(request, 'account/password/password_reset_done.html', {}) 
    else:
        return render(request, 'account/password/password_reset_form.html', {})


def reset_password_email(email, hash):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Licitamex"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": "Restablecer contraseña",
			"HTMLPart": f"""<h3>usted a solicitado cambiar contraseña.</h3>
			<br/>por favor da click en el link para cambiar tu contraseña<br/>
			<a href=\"https://consultalicitamex.com/account/set-new-password/?email={email}&hash={hash}\">consultalicitamex</a>"""
		}]
	}
	mailjet.send.create(data=data)


def reset_new_password(request, hash):
    user_form = ChangePasswordForm(request.POST)
    if request.method == "POST":
        password = request.POST.get('password')
        user = CustomUser.objects.filter(reset_passowrd_hash=hash)
        if user and user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['confirma_password']:
            u = user[0]
            u.reset_passowrd_hash = ""
            u.set_password(password)
            u.save()
            return render(request, 'account/password/password_reset_success.html', {})
        else:
            return render(request, 'account/password/new_password_form.html', {'form': user_form, "hash":hash})
    else:
        return render(request, 'account/password/new_password_form.html', {'form': user_form, "hash":hash})

def set_new_password(request):
    if request.method == "GET":
        email = request.GET.get('email')
        hash = request.GET.get('hash')
        user = CustomUser.objects.filter(email=email)
        date =datetime.now()
        date = date.utcnow().timestamp()
        if float(hash) < date and user[0].reset_passowrd_hash == hash:
            form = ChangePasswordForm()
            return render(request, 'account/password/new_password_form.html', {'form': form, "hash":hash})
        else:
            return render(request, 'account/password/password_expired.html', {})


@login_required
def configuracion(request):
    usuario_filtros = get_user_filtros(request.user.id)
    return render(request, 'account/configuracion.html', {"filtros":usuario_filtros})


@login_required
@never_cache
def licitaciones(request):
    items = fetch_items_table("licitaciones")["Items"]
    dependencias = fetch_dependencias()["Items"]
    print("dependencias")
    print(dependencias)
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items, "dependencias":dependencias})



def my_login(request):
    user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if user is None:
        return render(request, 'account/login.html',{"errror":"error"})
    up = UserPlan.objects.filter(owner_user=user.id)
    if up[0].plan_active == False:
        return render(request, 'account/suspended_account.html',{})
    if user is not None:
        login(request, user)
        licitaciones = UsuarioLicitaciones.objects.filter(user=request.user.id)
        return render(request, 'account/dashboard.html',
                  {'section': 'dashboard', "licitaciones":licitaciones})

@login_required
def dashboard(request):
    licitaciones = UsuarioLicitaciones.objects.filter(user=request.user.id)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', "licitaciones":licitaciones})


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
            if request.POST.get('tipo') == "stripe":
                user = CustomUser.objects.create_user(username=user_form.data['username'], first_name=user_form.data['first_name'], last_name=user_form.data['last_name'], email=user_form.data['email'], password=user_form.data['password'])
                user.save()
                trial_date_end =datetime.now() + timedelta(days=30)
                stripe.api_key = settings.STRIPE_SECRET
                #session = stripe.checkout.Session.create(
                session = stripe.Subscription.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=f"https://consultalicitamex.com/" + 'account/register-done/?session_id={CHECKOUT_SESSION_ID}&user_id='+f"{user.id}&plan_type=Basica",
                cancel_url=f"https://consultalicitamex.com/" + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                trial_end = trial_date_end.utcnow().timestamp(),
                line_items=[
                        {
                            'price': settings.STRIPE_BASIC,
                            'quantity': 1,
                        }
                    ]
                )
                return render(request, 'account/stripe-checkout.html', {"checkout":session["id"], "public_key": settings.STRIPE_KEY})
            else:
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
                            "return_url": "https://consultalicitamex.com/account/register-done/?type=paypal",
                            "cancel_url": "https://consultalicitamex.com/cancel/"
                        }
                    }
                    ret = myapi.post("v1/billing/subscriptions", data)
                    print("viendo status")
                    print(ret)
                    if ret['status'] == 'APPROVAL_PENDING':
                        # Create inactive user and profile

                        for link in ret['links']:
                            if link['rel'] == 'approve':
                                redirect_url = link['href']
                                user = CustomUser.objects.create_user(username=user_form.data['username'], first_name=user_form.data['first_name'], last_name=user_form.data['last_name'], email=user_form.data['email'], password=user_form.data['password'])
                                user.save()
                                up = UserPlan()
                                up.owner_user = user
                                up.type = request.session.get('subscription_plan')
                                up.status = "active"
                                up.plan_active = True
                                up.save()
                    
                        return HttpResponseRedirect(redirect_url)
                    #return HttpResponseRedirect("http://127.0.0.1:8000/")
                    #return render(request, 'account/dashboard.html',{})

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
                send_mail(subject, message, 'ruvalcaba91@hotmail.com',
                          ['ruvalcaba91@hotmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            # return redirect ('../../account/contact_message_done.html')
            return render(request, 'account/contact_message_done.html', {'form': form})

    form = ContactForm()
    return render(request, "account/contact.html", {'form': form})

class RegisterDonePageView(TemplateView):
    print("probando")
    template_name = 'account/register_done.html'



def registro_exitoso_email(email):
	mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')
	data = {
		'Messages': [{
			"From": {
				"Email": "norma.contreras@nilaconsulting.com.mx",
				"Name": "Licitamex"
			},
			"To": [{
				"Email": email,
				"Name": "You"
			}],
			"Subject": "Registro Exitoso",
			"HTMLPart": f"""<h3>Gracias por registrarte en LICITAMEX.</h3>
			<br/>Empieza a usar tu cuenta aqui.<br/>
			<a href=\"https://consultalicitamex.com/\">consultalicitamex</a>"""
		}]
	}
	mailjet.send.create(data=data)

def RegisterDone(request):
    type = request.GET.get('type')
    if type == "paypal":
        return render(request, "account/register_done.html")
    print("probando")
    user_id = request.GET.get('user_id')
    session_id = request.GET.get('session_id')
    plan_type = request.GET.get('plan_type')
    print("viendo el  id", user_id)
    print("viendo el  session_id", session_id)
    stripe.api_key = settings.STRIPE_SECRET
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)
    if session["payment_status"] in ["paid", "unpaid"]:
        print("si callo")
        user = CustomUser.objects.get(pk=user_id)
        up = UserPlan()
        up.owner_user = user
        up.type = plan_type
        up.status = "active"
        up.plan_active = True
        up.save()
        registro_exitoso_email(user.email)
    return render(request, "account/register_done.html")

def cancel(request):
    return render(request, "account/cancel.html")
