from django import forms
from django.contrib.auth.models import User
from .models import Profile

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
    #password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    plans = forms.ChoiceField(choices=subscription_options)
    tipo = forms.ChoiceField(choices=payment_types)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password')
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'password': 'Contraseña',
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
        model = Profile
        fields = ('company',)
