# Formulario
from django import forms

# Models
from apps.accountings.models import Insurance


# Tiempo
from datetime import datetime

class SeguroForm(forms.ModelForm):

    class Meta:
        model = Insurance
        
        fields = [
            'nombre_acreedor',
        'fecha_inicio',
        'monto',
        'tasa',
        'plazo',
        'numero_referencia',
        'observaciones',
        'boleta',
        'credito'
        ]

        labels = {
            'nombre_acreedor':'Nombre',
            'fecha_inicio': 'Fecha de Inicio',
            'monto': 'Monto Otorgado',
            'tasa': 'Tasa',
            'plazo':'Plazo',
            'numero_referencia':'Numero de Referencia',
            'observaciones': 'Observaciones',
            'boleta':'Boleta',
            'credito':'Credito'
        }

        widgets = {
            'nombre_acreedor': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'fecha_inicio': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tasa': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'plazo': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0'}),
            'numero_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}),  
            'credito':forms.Select(attrs={'class':'form-control credito_vigente'})
        }