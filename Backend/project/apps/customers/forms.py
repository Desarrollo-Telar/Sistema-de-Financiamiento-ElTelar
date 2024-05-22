# Formulario
from django import forms

# Models
from .models import Customer, ImmigrationStatus

# Validaciones
from project.validations import validar_correo, validar_numero_telefono

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        
        fields = [
            'first_name',
            'last_name',
            'type_identification',
            'identification_number',
            'telephone',
            'email'
        ]

        labels = {}

        widgets = {}