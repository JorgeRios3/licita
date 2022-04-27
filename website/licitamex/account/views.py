import grp
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, ContactForm, ChangePasswordForm, NewUserForm
from .models import UsuarioLicitaciones, CustomUser, Group, UsuarioPermisos, Permiso
from django.contrib.auth.models import User
import paypalrestsdk
import json
from paypalrestsdk.notifications import WebhookEvent
from .dynamo_functions import fetch_items_table, fetch_dependencias
from .licitaciones import get_user_licitaciones
from .filtros import get_user_filtros
from .utils import compare_user
#from django.http import JsonResponse
from django.views.decorators.cache import never_cache
import stripe
from django.views.generic import TemplateView
from datetime import datetime
from datetime import timedelta
#from django.urls import reverse
from .mails import reset_password_email, registro_exitoso_email
from django.contrib.auth import logout
import requests
from requests.auth import HTTPBasicAuth
from .utils import account_is_active
from .configuracion_data import data_configuracion







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
def borrar_cuenta(request):
    user = CustomUser.objects.filter(pk=request.user.id)
    group = Group.objects.filter(pk=user[0].group.id)
    group = group[0]
    if int(group.admin_user) != int(request.user.id):
        return HttpResponse("necesitas derecho de administrador para poder borrar")
    if request.method == "POST":
        print("borrando la cuenta")
        logout(request)
        stripe.api_key = settings.STRIPE_SECRET
        if group.payment_vendor == "Stripe":
            val = stripe.Subscription.delete(group.subscription_id)
            group.plan_is_active = False
            group.save()
            print(val)
            return HttpResponse(status=200)
        else:
            ret = myapi.post("v1/billing/subscriptions/{}/cancel".format(group.subscription_id))
            print("viendo cancelacion  ", ret)
            group.plan_is_active = False
            group.save()
            return HttpResponse(status=200)

    else:
        return render(request, 'account/borrar_cuenta.html', {})


@login_required
@account_is_active
def configuracion(request):
    data = data_configuracion(request)
    return render(request, 'account/configuracion.html', {"filtros":data["filtros"], 
    "form":data["form"], "usuarios":data["usuarios"], "group":data["group"], 
    "is_admin":data["is_admin"], "permisos_usuarios":data["permisos_usuarios"], "permisos":data["permisos"]})


@login_required
@never_cache
@account_is_active
def licitaciones(request):
    items = fetch_items_table("licitaciones")["Items"]
    dependencias = fetch_dependencias()["Items"]
    print("dependencias")
    print(dependencias)
    user_licitaciones = get_user_licitaciones(request.user.id)
    validated_items = list(map(lambda x: compare_user(x, user_licitaciones), items))
    return render(request, 'account/licitaciones.html', {"licitaciones":validated_items, "dependencias":dependencias})



def my_login(request):
    print("en login")
    user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    print("viendo user ",user)
    if user is None:
        return render(request, 'account/login.html',{"errror":"error"})
    group = Group.objects.filter(owner_user=user.group)
    if group[0].plan_is_active == False:
        return render(request, 'account/suspended_account.html',{})
    if user is not None:
        login(request, user)
        licitaciones = UsuarioLicitaciones.objects.filter(user=request.user.id)
        return render(request, 'account/dashboard.html',
                  {'section': 'dashboard', "licitaciones":licitaciones})

@login_required
@account_is_active
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
        print("si entrooo")
        user_form = UserRegistrationForm(request.POST)
        users = CustomUser.objects.filter(email = user_form.data['email'])
        print("esto ", len(users))
        if len(users) >0:
            return render(request, 'account/user_exists.html', {})
        if user_form.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')
            print("aqui")
            if request.POST.get('tipo') == "stripe":
                if request.session.get('subscription_plan') == 'Basica':
                    group = Group()
                    company = user_form.data['email'].split("@")[0]
                    group.company = company
                    group.save()
                    user = CustomUser.objects.create_user(username=user_form.data['username'], first_name=user_form.data['first_name'], last_name=user_form.data['last_name'], email=user_form.data['email'], password=user_form.data['password'], group=group)
                    user.save()
                    permiso = Permiso.objects.filter(permiso='administrador')
                    permiso = permiso[0]
                    up = UsuarioPermisos()
                    up.usuario=user
                    up.permiso = permiso
                    up.group = group
                    up.save()
                    trial_date_end =datetime.now() + timedelta(days=30)
                    stripe.api_key = settings.STRIPE_SECRET
                    session = stripe.checkout.Session.create(
                    client_reference_id=request.user.id if request.user.is_authenticated else None,
                    success_url=f"https://consultalicitamex.com/" + 'account/register-done/?session_id={CHECKOUT_SESSION_ID}&group_id='+f"{group.id}&subscription_type=Basica&user_id{user.id}",
                    cancel_url=f"https://consultalicitamex.com/" + 'cancel/',
                    #success_url=f"http://127.0.0.1:8000/" + 'account/register-done/?session_id={CHECKOUT_SESSION_ID}&group_id='+f"{group.id}&subscription_type=Basica&user_id={user.id}",
                    #cancel_url=f"http://127.0.0.1:8000/" + 'cancel/',
                    payment_method_types=['card'],
                    mode='subscription',
                    #trial_end = trial_date_end.utcnow().timestamp(),
                    line_items=[
                            {
                                'price': settings.STRIPE_BASIC,
                                'quantity': 1,
                            }
                        ]
                    )
                    return render(request, 'account/stripe-checkout.html', {"checkout":session["id"], "public_key": settings.STRIPE_KEY})
            else:
                print("aca")
                group = Group()
                company = user_form.data['email'].split("@")[0]
                group.company = company
                group.save()
                print(request.session.get('subscription_plan'))
                if request.session.get('subscription_plan') == 'Basica':
                    plan_id = settings.PAYPAL_PLAN_MONTHLY_ID
                    data = {
                        'plan_id': plan_id,
                        "subscriber": {
                            "name": {
                            "given_name": user_form.data['first_name'],
                            "surname": user_form.data['last_name']
                            },
                            "email_address": user_form.data['email'].strip()
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
                                user = CustomUser.objects.create_user(username=user_form.data['username'], first_name=user_form.data['first_name'], last_name=user_form.data['last_name'], email=user_form.data['email'], password=user_form.data['password'],group=group)
                                user.save()
                                group.plan_is_active = True
                                group.admin_user = user.id
                                group.subscription_type = "Basica"
                                group.payment_vendor = "Paypal"
                                group.subscription_id = ret["id"] #session["subscription"]
                                group.save()
                                permiso = Permiso.objects.filter(permiso='administrador')
                                permiso = permiso[0]
                                up = UsuarioPermisos()
                                up.usuario=user
                                up.permiso = permiso
                                up.group = group
                                up.save()
                    
                        return HttpResponseRedirect(redirect_url)
                    #return HttpResponseRedirect("http://127.0.0.1:8000/")
                    #return render(request, 'account/dashboard.html',{})

    else:
        print("no es valida")
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


def RegisterDone(request):
    type = request.GET.get('type')
    if type == "paypal":
        return render(request, "account/register_done.html")
    print("probando")
    group_id = request.GET.get('group_id')
    session_id = request.GET.get('session_id')
    subscription_type = request.GET.get('subscription_type')
    user_id = request.GET.get('user_id')
    print("viendo el  id", user_id)
    print("viendo el  session_id", session_id)
    stripe.api_key = settings.STRIPE_SECRET
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)
    if session["payment_status"] in ["paid", "unpaid"]:
        print("si callo")
        group = Group.objects.get(pk=group_id)
        group.plan_is_active = True
        group.admin_user = user_id
        group.subscription_type = subscription_type
        group.subscription_id = session["subscription"]
        group.payment_vendor = "Stripe"
        group.save()
        user = CustomUser.objects.get(pk=user_id)
        registro_exitoso_email(user.email)
    return render(request, "account/register_done.html")

def cancel(request):
    return render(request, "account/cancel.html")
