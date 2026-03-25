# Formulario
from django import forms

# Models
from apps.financings.models import Credit


# Tiempo
from datetime import datetime




class CreditoForms(forms.ModelForm):
    class Meta:
        model = Credit

        fields = [
            'proposito',
            'monto',
            'plazo',
            'fecha_inicio',
            'tasa_interes',
            'forma_de_pago',
            'tipo_credito',
            'tipo_proceso',
            'estado_judicial',
            'categoria_credito_demandado',
            'customer_id',
            'asesor_de_credito'
        ]

        labels = {
            'proposito': 'Proposito del Credito',
            'monto': 'Monto Otorgado',
            'fecha_inicio': 'Fecha de Inicio del Credito',
            'plazo': 'Plazo del Credito (Meses)',
            'tasa_interes': 'Tasa de Interes (Mensual)',
            'forma_de_pago': 'Forma de Pago',
            'tipo_proceso': 'Tipo de Proceso de Pago',
            'categoria_credito_demandado': 'Categoria del Credito Demandado',
            'estado_judicial': 'Credito Demandado',
            'tipo_credito':'Tipo de Credito',
            'customer_id': 'Cliente',
            'asesor_de_credito':'Asesor de Credito'
        }

        widgets = {
            'monto':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'tasa_interes':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'plazo':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
           
            'estado_judicial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'fecha_inicio':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proposito':forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'categoria_credito_demandado':forms.Select(attrs={'class':'form-control '}),
            'tipo_proceso': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'forma_de_pago': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'tipo_credito': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'customer_id':forms.Select(attrs={'class':'form-control customer_id'}),
            'asesor_de_credito':forms.Select(attrs={'class':'form-control asesor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_tipo_proceso = [
            
            ('NORMAL', 'NORMAL'),
            ('RECUPERACION PARCIAL CAPITAL', 'RECUPERACION PARCIAL CAPITAL'),
            ('RECUPERACION TOTAL CAPITAL', 'RECUPERACION TOTAL CAPITAL'),
            
        ]

        opciones_forma_de_pago = [        
            ('NIVELADA', 'NIVELADA'),
            ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL'),
            ('INTERES MENSUAL Y CAPITAL AL VENCIMIENTO', 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO'),
            ('INTERES Y CAPITAL AL VENCIMIENTO', 'INTERES Y CAPITAL AL VENCIMIENTO')

        ]
        opciones_tipo_credito = [
            ('AGROPECUARIO Y/O PRODUCTIVO', 'AGROPECUARIO Y/O PRODUCTIVO'),
            ('COMERCIO', 'COMERCIO'),
            ('SERVICIOS', 'SERVICIOS'),
            ('CONSUMO', 'CONSUMO'),
            ('VIVIENDA', 'VIVIENDA')
        ]


        # Asignar las opciones al widget 'Select'
        self.fields['tipo_proceso'].widget.choices = opciones_tipo_proceso
        self.fields['forma_de_pago'].widget.choices = opciones_forma_de_pago
        self.fields['tipo_credito'].widget.choices = opciones_tipo_credito

        date_fields = ['fecha_inicio']

        for field in date_fields:
            self.fields[field].input_formats = ['%Y-%m-%d']


class CreditoMigradoForms(forms.ModelForm):
    class Meta:
        model = Credit

        fields = [
            'proposito',
            'monto',
            'plazo',
            'fecha_inicio',
            'tasa_interes',
            'forma_de_pago',
            'tipo_credito',
            'tipo_proceso',
            'estado_judicial',
            'categoria_credito_demandado',
            
        ]

        labels = {
            'proposito': 'Proposito del Credito',
            'monto': 'Monto Otorgado',
            'fecha_inicio': 'Fecha de Inicio del Credito',
            'plazo': 'Plazo del Credito (Meses)',
            'tasa_interes': 'Tasa de Interes (Mensual)',
            'forma_de_pago': 'Forma de Pago',
            'tipo_proceso': 'Tipo de Proceso de Pago',
            'categoria_credito_demandado': 'Categoria del Credito Demandado',
            'estado_judicial': 'Credito Demandado',
            'tipo_credito':'Tipo de Credito',
            'customer_id': 'Cliente',
            'asesor_de_credito':'Asesor de Credito'
        }

        widgets = {
            'monto':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'tasa_interes':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
            'plazo':forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0','step':'any'}),
           
            'estado_judicial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'fecha_inicio':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proposito':forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'categoria_credito_demandado':forms.Select(attrs={'class':'form-control '}),
            'tipo_proceso': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'forma_de_pago': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'tipo_credito': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'customer_id':forms.Select(attrs={'class':'form-control customer_id'}),
            'asesor_de_credito':forms.Select(attrs={'class':'form-control asesor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_tipo_proceso = [
            
            ('NORMAL', 'NORMAL'),
            ('RECUPERACION PARCIAL CAPITAL', 'RECUPERACION PARCIAL CAPITAL'),
            ('RECUPERACION TOTAL CAPITAL', 'RECUPERACION TOTAL CAPITAL'),
            
        ]

        opciones_forma_de_pago = [        
            ('NIVELADA', 'NIVELADA'),
            ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL'),
            ('INTERES MENSUAL Y CAPITAL AL VENCIMIENTO', 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO'),
            ('INTERES Y CAPITAL AL VENCIMIENTO', 'INTERES Y CAPITAL AL VENCIMIENTO')

        ]
        opciones_tipo_credito = [
            ('AGROPECUARIO Y/O PRODUCTIVO', 'AGROPECUARIO Y/O PRODUCTIVO'),
            ('COMERCIO', 'COMERCIO'),
            ('SERVICIOS', 'SERVICIOS'),
            ('CONSUMO', 'CONSUMO'),
            ('VIVIENDA', 'VIVIENDA')
        ]


        # Asignar las opciones al widget 'Select'
        self.fields['tipo_proceso'].widget.choices = opciones_tipo_proceso
        self.fields['forma_de_pago'].widget.choices = opciones_forma_de_pago
        self.fields['tipo_credito'].widget.choices = opciones_tipo_credito

        date_fields = ['fecha_inicio']

        for field in date_fields:
            self.fields[field].input_formats = ['%Y-%m-%d']