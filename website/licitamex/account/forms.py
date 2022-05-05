from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Group
from .models import CustomUser

subscription_options = [
        ('Basica', 'Membresía basica ($249.00 MX/Mes)'),
    ]

payment_types = [
        ('paypal', 'Paypal'),
        ('stripe', 'Stripe')
    ]

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password.widget.attrs.update({'class' : 'basic-input'})
    confirma_password = forms.CharField(widget=forms.PasswordInput())
    confirma_password.widget.attrs.update({'class' : 'basic-input'})


    class Meta:
        model = CustomUser
    
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirma_password")

        if password != confirm_password:
            self.add_error('confirma_password', "Las contraseñas no coinciden")

        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50, required=True)
    email = forms.EmailField(max_length = 150, required=True)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000, required=True)
    

class UserRegistrationForm(forms.ModelForm):
    plans = forms.ChoiceField(choices=subscription_options)
    plans.widget.attrs.update({'class' : 'basic-input'})
    tipo = forms.ChoiceField(choices=payment_types)
    tipo.widget.attrs.update({'class' : 'basic-input'})
    acceptar_terminos_y_condiciones = forms.BooleanField(required=True)


    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','password')
        widgets = {
           "username": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Usuario", 'required': 'true' }),
           "first_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Nombres", 'required': 'true' }),
           "last_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Apellidos", 'required': 'true' }),
           "email": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Email", 'required': 'true' }),
           "password": forms.PasswordInput(attrs={'class': 'basic-input', "placeholder":"Contraseña", 'required': 'true' }),
           #"": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Apellidos", 'required': 'true' }),

        }



class NewUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', "password")
        widgets = {
           "username": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Usuario", 'required': 'true' }),
           "first_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Nombres", 'required': 'true' }),
           "last_name": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Apellidos", 'required': 'true' }),
           "email": forms.TextInput(attrs={'class': 'basic-input', "placeholder":"Email", 'required': 'true'}),
           "password": forms.PasswordInput(attrs={'class': 'basic-input', "placeholder":"Contraseña", 'required': 'true' }),
        }

        def clean(self):
            cleaned_data = super(NewUserForm, self).clean()
            email = cleaned_data.get("email")
            if len(email)<2:
                self.add_error('email', "Las contraseñas no coinciden")

            return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
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
