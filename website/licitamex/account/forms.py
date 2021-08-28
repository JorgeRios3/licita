from django import forms
from django.contrib.auth.models import User
from .models import Profile

subscription_options = [
        ('Basica', 'Membresia basica ($10 MX/Mes)')
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
    plan = forms.ChoiceField(choices=subscription_options)
    tipo_de_pago = forms.ChoiceField(choices=payment_types)


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
    
    #def clean_password2(self):
    #    cd = self.cleaned_data
    #    if cd['password'] != cd['password2']:
    #        raise forms.ValidationError('Las contraseñas no coinciden')
    #    return cd['password2']
        

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
