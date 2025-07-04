# Formulario
from django import forms

# Models
from apps.accountings.models import Egress


# Tiempo
from datetime import datetime

from django import forms


class EgresoForm(forms.ModelForm):
    monto_doc = forms.DecimalField(
        required=False,  # Permite que el campo sea opcional
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
        label='Monto del Documento'
    )

    class Meta:
        model = Egress
        fields = [
            'codigo_egreso',
            'fecha',
            'fecha_doc_fiscal',
            'numero_doc',
            'nit',
            'monto',
            'monto_doc',
            'numero_referencia',
            'descripcion',
            'observaciones',
            'boleta',
            'documento',
            'nombre',
            'pago_correspondiente',
            'tipo_impuesto',
            'tipo_gasto'
        ]
        labels = {
            'fecha': 'Fecha',
            'fecha_doc_fiscal': 'Fecha del Documento Fiscal',
            'numero_doc': 'Numero de Documento',
            'nit': 'NIT',
            'monto': 'Monto',
            'monto_doc': 'Monto del Documento',
            'numero_referencia': 'Numero de Referencia',
            'codigo_egreso': 'Codigo de Egreso',
            'descripcion': 'Descripcion',
            'observaciones': 'Observaciones',
            'boleta': 'Boleta',
            'documento': 'Documento',
            'nombre': 'Nombre del Colaborador',
            'pago_correspondiente': 'Pago Correspondiente',
            'tipo_gasto': 'Tipo de Gastos',
            'tipo_impuesto': 'Tipo de Impuesto'
        }
        widgets = {
            'fecha': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_doc_fiscal': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
            'numero_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_egreso': forms.Select(choices=[], attrs={'class': 'form-control'}),  # Se definirá más adelante.
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'boleta': forms.FileInput(attrs={'type': 'file', 'class': 'form-control', 'accept': '.pdf, .doc, .docx, .xls, .xlsx, .txt, image/*'}),
            'documento': forms.FileInput(attrs={'type': 'file', 'class': 'form-control', 'accept': '.pdf, .doc, .docx, .xls, .xlsx, .txt, image/*'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'pago_correspondiente': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_gasto': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_impuesto': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_codigo_ingreso = [
            ('', 'Seleccione un código'),  # Opción inicial
            ('SALARIOS', 'SALARIOS'),
            ('ALQUILER', 'ALQUILER'),
            ('GASTOS POR DESEMBOLSOS', 'GASTOS POR DESEMBOLSOS'),
            ('OTROS GASTOS GENERALES', 'OTROS GASTOS GENERALES'),
            ('COMBUSTIBLES', 'COMBUSTIBLES'),
            ('PAPELERIA Y UTILES', 'PAPELERIA Y UTILES'),
            ('ALIMENTACIÓN', 'ALIMENTACIÓN'),
            ('GASTOS DE MANTENIMIENTO', 'GASTOS DE MANTENIMIENTO'),
            ('EQUIPO DE COMPUTACIÓN', 'EQUIPO DE COMPUTACIÓN'),
            ('PAGO DE IMPUESTOS', 'PAGO DE IMPUESTOS'),
            ('SERVICIOS TERCEROS', 'SERVICIOS TERCEROS'),
            ('COMUNICACIONES', 'COMUNICACIONES'),
        ]

        # Asignar las opciones al widget 'Select'
        self.fields['codigo_egreso'].widget.choices = opciones_codigo_ingreso


       