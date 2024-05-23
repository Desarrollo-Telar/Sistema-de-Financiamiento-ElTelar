# Formulario
from django import forms

# Models
from .models import Customer, ImmigrationStatus

# Validaciones
from project.validations import validar_correo, validar_numero_telefono
# Tiempo
from datetime import datetime
class CustomerForm(forms.ModelForm):
    email = forms.EmailField(
        label="Correo Electronico",
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}),
        required=True

    )
    telephone = forms.CharField(
        label='Numero de telefono',
        widget=forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not validar_correo(email):
            raise forms.ValidationError('El formato del correo electrónico no es válido.')
        
        return email
    
    def clean_telephone(self):
        telephone = self.changed_data.get('telephone')

        if not validar_numero_telefono(telephone):
            raise forms.ValidationError('El numero de telefono no es válido.')

        return telephone

    class Meta:
        model = Customer
        
        fields = [
            'first_name',
            'last_name',
            'type_identification',
            'identification_number',
            'marital_status',            
            'nationality',
            'number_nit',
            'date_birth',
            'place_birth',
            'gender',
            'profession_trade',
            'person_type',
            'telephone',
            'email',
            'status',  
        ]

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'type_identification': 'Tipo de Identificación',
            'identification_number': 'Numero de Identificación',
            'person_type': 'Tipo de Persona',             
            'status': 'Status del cliente',
            'date_birth': 'Fecha de Nacimiento',
            'number_nit': 'Numero de NIT',
            'place_birth': 'Lugar de Nacimiento',
            'marital_status': 'Estado Civil',
            'profession_trade': 'Profesión u Oficio',
            'gender': 'Genero',
            'nationality': 'Nacionalidad',
            
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_identification': forms.Select(attrs={'class': 'form-control'}),
            'identification_number': forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'person_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date_birth': forms.TextInput(attrs={'type':'date', 'class':'form-control'}),
            'number_nit':forms.TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'place_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.TextInput(attrs={'class': 'form-control'}),
            'profession_trade': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),

        }