# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username_or_email = forms.CharField(label='Nombre de usuario o correo electrónico')

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Verifica si el valor ingresado es un correo electrónico
            if '@' in username_or_email:
                # Si es un correo electrónico, establece el campo de nombre de usuario en el correo electrónico
                self.cleaned_data['username'] = username_or_email
            else:
                # Si no es un correo electrónico, establece el campo de nombre de usuario en el valor ingresado
                self.cleaned_data['username'] = username_or_email
        return super().clean()
