from django import forms

# modelo
from apps.customers.models import Cobranza

class CobranzaForms(forms.ModelForm):
    class Meta:
        model = Cobranza
        
        fields = [
            'credito',
            
            'mora_pendiente',            
            'interes_pendiente',
            'monto_pendiente',
            'telefono_contacto',

            'tipo_cobranza',
            'fecha_gestion',
            'tipo_gestion',
            'resultado',
            
            'fecha_promesa_pago',
            'observaciones',
            'estado_cobranza'
            
        ]

        labels = {
            'credito': 'Credito En Gestion',
            'cuota':'Cuota',
            'tipo_cobranza': 'Tipo de Cobranza',
            'fecha_gestion': 'Fecha de la Gestion',
            'tipo_gestion': 'Tipo de Gestion',
            'resultado': 'Resultado Obtenido',
            'monto_pendiente': 'Monto Pendiente A Cancelar',
            'interes_pendiente': 'Total de Interes Pendientes',
            'mora_pendiente': 'Total de Mora Pendiente',
            'fecha_promesa_pago': 'Fecha Promesa de Pago',
            'observaciones': 'Observaciones',
            'estado_cobranza': 'Estado de la cobranza',
            'telefono_contacto': 'Numero de Telefono del Cliente'

        }

        widgets = {
            'credito': forms.Select(attrs={'class':'form-control credito_vigente'}),
            'cuota': forms.Select(attrs={'class':'form-control', 'disabled':'disabled'}),
            'tipo_cobranza': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'fecha_gestion':forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_gestion':  forms.Select(choices=[], attrs={'class': 'form-control'}),
            'resultado': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'monto_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
            'interes_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
            'mora_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
            'fecha_promesa_pago': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado_cobranza':forms.Select(choices=[], attrs={'class': 'form-control'}),
            'telefono_contacto':forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_tipo_cobranza = [
            ('', 'Seleccione un Tipo de Cobranza'),  # Opción inicial
            ('preventiva', 'Preventiva'),
            ('normal', 'Normal'),
            ('castigada', 'Castigada'),
            ('judicial', 'Judicial'),
            
        ]

        opciones_tipo_gestion = [
            ('', 'Seleccione un Tipo de Gestion'),  # Opción inicial
            ('llamada', 'Llamada'),
            ('whatsapp', 'WhatsApp'),
            ('visita', 'Visita presencial'),
            ('correo', 'Correo electrónico'),

        ]

        opciones_resultados = [
            ('', 'Seleccione un Tipo de Resultado'),  # Opción inicial
            ('promesa_pago', 'Promesa de pago'),
            ('pago_realizado', 'Pago realizado'),
            ('no_localizado', 'No localizable'),
            ('negativa_pago', 'Negativa de pago'),
            
        ]

        opciones_estado_cobranza = [
            ('', 'Seleccione un Tipo de Resultado'),  # Opción inicial
            ('pendiente', 'Pendiente'),
            ('gestionado', 'Gestionado'),
            ('incumplido', 'Incumplido'),
            ('cerrado', 'Cerrado'),

        ]

        # Asignar las opciones al widget 'Select'
        self.fields['tipo_cobranza'].widget.choices = opciones_tipo_cobranza
        self.fields['tipo_gestion'].widget.choices = opciones_tipo_gestion
        self.fields['resultado'].widget.choices = opciones_resultados
        self.fields['estado_cobranza'].widget.choices = opciones_estado_cobranza