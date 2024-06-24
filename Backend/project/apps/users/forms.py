from django import forms

# Modelo
from .models import User

# LIBRERIA QUE SE ENCARGA DE CREAR USUARIOS
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Validaores
from .validations import validar_correo

### -- FORMULARIO PARA CREAR USUARIOS--#
# Formulario
class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=True
    )

    email = forms.EmailField(
        label="Correo Electronico",
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}),
        required=True

    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off'}),
        required=True,


    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off'}),
        required=True,


    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        
        if not validar_correo(email):
            raise forms.ValidationError('El formato del correo electrónico no es válido.')
        
        return email

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'type_identification',
            'identification_number',
            'telephone',
            'gender',
            'nationality',
            'profile_pic',
            'rol'

        ]

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'type_identification':'Tipo de Identificación',
            'identification_number': 'Numero de Identificación',
            'telephone': 'Numero de Telefono',
            'gender':'Genero',
            'nationality':'Nacionalidad',
            'profile_pic':'Imagen de Usuario',
            'rol':'Rol de Usuario'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'name': 'telefono'}),
            'type_identification': forms.Select(attrs={'class':'form-control', 'name':'type_identification', 'id':'type_identification'}),
            'identification_number':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'gender': forms.Select(attrs={'class':'form-control', 'name':'gender', 'id':'gender'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'name':'image', 'type':'file', 'accept':'image/*', 'class':'form-control'}),
            'rol':forms.Select(attrs={'class':'form-control', 'name':'rol', 'id':'rol'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'type_identification', 'identification_number', 'telephone', 'status', 'gender', 'user_code', 'nationality', 'profile_pic','rol')

class UpdateUserForm(forms.ModelForm):
   

    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        required=True
    )

    email = forms.EmailField(
        label="Correo Electronico",
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}),
        required=True

    )

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not validar_correo(email):
            raise forms.ValidationError('El formato del correo electrónico no es válido.')
        
        return email
    

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'type_identification',
            'identification_number',
            'telephone',
            'gender',
            'nationality',
            'profile_pic',
            'rol'

            
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'type_identification':'Tipo de Identificación',
            'identification_number': 'Numero de Identificación',
            'telephone': 'Numero de Telefono',
            'gender':'Genero',
            'nationality':'Nacionalidad',
            'status': 'Estado',
            'profile_pic':'Imagen de Usuario',
            'rol':'Rol de Usuario',

        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'type_identification': forms.Select(attrs={'class':'form-control', 'name':'type_identification', 'id':'type_identification'}),
            'identification_number':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'gender': forms.Select(attrs={'class':'form-control', 'name':'gender', 'id':'gender'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'type':'checkbox', 'name':'image', 'type':'file', 'accept':'image', 'class':'form-control'}),
            'rol':forms.Select(attrs={'class':'form-control', 'name':'rol', 'id':'rol'}),
        }

###-- FORMULARIO PARA CAMBIAR LA CONTRASEÑA --###
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='NUEVA CONTRASEÑA: ',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        required = True,
       

    )
    password2 = forms.CharField(
        label='CONFIRMAR CONTRASEÑA: ',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        required = True,       


    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Contraseña no coinciden')
        return password2