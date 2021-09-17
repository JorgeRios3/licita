from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Group

subscription_options = [
        ('Basica', 'Membresia basica ($10 MX/Mes)'),
    ]

payment_types = [
        ('paypal', 'Paypal'),
        ('stripe', 'Stripe')
    ]

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, required=True)
    email = forms.EmailField(max_length = 150, required=True)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000, required=True)
    

class UserRegistrationForm(forms.ModelForm):
    plans = forms.ChoiceField(choices=subscription_options)
    plans.widget.attrs.update({'class' : 'basic-input'})
    tipo = forms.ChoiceField(choices=payment_types)
    tipo.widget.attrs.update({'class' : 'basic-input'})


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password')
        widgets = {
           "username": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Usuario", 'required': 'true' }),
           "first_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Nombres", 'required': 'true' }),
           "last_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Apellidos", 'required': 'true' }),
           "email": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Email", 'required': 'true' }),
           "password": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Contraseña", 'required': 'true' }),
        }
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'password': 'Contraseña',
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('company',)
