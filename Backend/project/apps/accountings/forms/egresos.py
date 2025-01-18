# Formulario
from django import forms

# Models
from apps.accountings.models import Egress


# Tiempo
from datetime import datetime

from django import forms


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egress
        fields = [
            'fecha',
            'fecha_doc_fiscal',
            'numero_doc',
            'nit',
            'monto',
            'monto_doc',
            'numero_referencia',
            'codigo_egreso',
            'descripcion',
            'observaciones',
            'boleta',
            'documento'
        ]
        labels = {
            'fecha': 'Fecha',
            'fecha_doc_fiscal': 'Fecha del Documento Fiscal',
            'numero_doc': 'Numero de Documento',
            'nit': 'NIT',
            'monto': 'Monto',
            'monto_doc': 'Monto del Documento',
            'numero_referencia':'Numero de Referencia',
            'codigo_egreso': 'Codigo de Egreso',
            'descripcion': 'Descripcion',
            'observaciones': 'Observaciones',
            'boleta': 'Boleta',
            'documento': 'Documento'
        }
        widgets = {
            'fecha': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_doc_fiscal': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'monto_doc': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'numero_referencia': forms.TextInput(attrs={'class': 'form-control'}),

            'codigo_egreso': forms.Select(choices=[],attrs={'class': 'form-control'}),  # Se definirá más adelante.
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            
            'boleta':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}),  
            'documento':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt,image/*'}), 
        }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_codigo_ingreso = [
            ('', 'Seleccione un código'),  # Opción inicial
            ('OTROS GASTOS GENERALES', 'OTROS GASTOS GENERALES'),
            ('COMBUSTIBLES', 'COMBUSTIBLES'),
            ('ALIMENTACIÓN', 'ALIMENTACIÓN'),
            ('GASTOS DE MANTENIMIENTO', 'GASTOS DE MANTENIMIENTO'),
            ('SERVICIOS TERCEROS', 'SERVICIOS TERCEROS'),
            ('PAPELERIA Y UTILES', 'PAPELERIA Y UTILES'),
            ('EQUIPO DE COMPUTACIÓN', 'EQUIPO DE COMPUTACIÓN'),
            ('GASTOS ADMINISTRATIVOS', 'GASTOS ADMINISTRATIVOS'),
            ('SALARIOS', 'SALARIOS'),
            ('PAGO DE IMPUESTOS', 'PAGO DE IMPUESTOS'),
            ('ALQUILER', 'ALQUILER'),
            ('COMUNICACIONES', 'COMUNICACIONES'),
            ('ACREEDORES', 'ACREEDORES'),
            ('GASTOS POR DESEMBOLSOS', 'GASTOS POR DESEMBOLSOS'),
            ('PAGO DE SEGUROS', 'PAGO DE SEGUROS')

        ]

        # Asignar las opciones al widget 'Select'
        self.fields['codigo_egreso'].widget.choices = opciones_codigo_ingreso


       