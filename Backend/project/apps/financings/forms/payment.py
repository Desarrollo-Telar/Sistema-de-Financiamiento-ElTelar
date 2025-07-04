# Formulario
from django import forms

# Models
from apps.financings.models import Payment


# Tiempo
from datetime import datetime

class BoletaForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'monto',
            'numero_referencia',
            'fecha_emision',
            'descripcion',
            'boleta',
            
        ]

        labels = {
            'monto':'Monto de la Boleta',
            'numero_referencia': 'Numero de Referencia',
            'fecha_emision': 'Fecha de Emision',
            'descripcion': 'Descripcion',
            'boleta': 'Boleta',
            'acreedor': 'Acreedor',
        }

        widgets = {
            'monto':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'numero_referencia':forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}), 
        }


class BoletaSeguroForm(forms.ModelForm):
    class Meta:
        model = Payment

        fields = [
            'seguro',
            'monto',
            'numero_referencia',
            'fecha_emision',
            'descripcion',
            'boleta',
            
        ]

        labels = {
            'monto':'Monto de la Boleta',
            'numero_referencia': 'Numero de Referencia',
            'fecha_emision': 'Fecha de Emision',
            'descripcion': 'Descripcion',
            'boleta': 'Boleta',
            'seguro': 'Seguro',
        }

        widgets = {
            'monto':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'numero_referencia':forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'seguro':forms.Select(attrs={'class':'form-control seguro'}),
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}), 
        }

class BoletaAcreedorForm(forms.ModelForm):
    class Meta:
        model = Payment

        fields = [
            'acreedor',
            'monto',
            'numero_referencia',
            'fecha_emision',
            'descripcion',
            'boleta',
            
        ]

        labels = {
            'monto':'Monto de la Boleta',
            'numero_referencia': 'Numero de Referencia',
            'fecha_emision': 'Fecha de Emision',
            'descripcion': 'Descripcion',
            'boleta': 'Boleta',
            'acreedor': 'Acreedor',
        }

        widgets = {
            'monto':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'numero_referencia':forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'acreedor':forms.Select(attrs={'class':'form-control acreedor'}),
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}), 
        }