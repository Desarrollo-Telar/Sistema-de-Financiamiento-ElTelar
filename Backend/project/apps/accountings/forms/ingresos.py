# Formulario
from django import forms

# Models
from apps.accountings.models import Income


# Tiempo
from datetime import datetime

from django import forms


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'fecha',
            'monto',
            'numero_referencia',
            'codigo_ingreso',
            'descripcion',
            'observaciones',
            
            'boleta'
        ]
        labels = {
            'fecha': 'Fecha',
            'monto': 'Monto',
            'codigo_ingreso': 'Código de Ingreso',
            'descripcion': 'Descripción',
            'observaciones': 'Observaciones',
            'numero_referencia': 'Número de Referencia',
            'boleta': 'Boleta'
        }
        widgets = {
            'fecha': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'codigo_ingreso': forms.Select(choices=[],attrs={'class': 'form-control'}),  # Se definirá más adelante.
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'numero_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}),  
        }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_codigo_ingreso = [
            ('', 'Seleccione un código'),  # Opción inicial
            ('Servicios terceros', 'Servicios terceros'),
            ('Otros Ingresos', 'Otros Ingresos'),
        ]

        # Asignar las opciones al widget 'Select'
        self.fields['codigo_ingreso'].widget.choices = opciones_codigo_ingreso


       