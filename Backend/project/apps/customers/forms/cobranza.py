from django import forms

# modelo
from apps.customers.models import Cobranza

class CobranzaForms(forms.ModelForm):
    class Meta:
        model = Cobranza
        
        fields = [
            'credito', 
            'fecha_limite_cuota',           
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
            'estado_cobranza',
            
            
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
            'fecha_promesa_pago': 'Fecha Promesa de Pago O Fecha de Seguimiento',
            'observaciones': 'Observaciones',
            'estado_cobranza': 'Estado de la cobranza',
            'telefono_contacto': 'Numero de Telefono del Cliente',
            'fecha_limite_cuota': 'Fecha De Limite Para La Cuota',
            

        }

        widgets = {
            'credito': forms.Select(attrs={'class':'form-control credito_vigente'}),
            'cuota': forms.Select(attrs={'class':'form-control', 'disabled':'disabled'}),
            'tipo_cobranza': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'fecha_gestion':forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_gestion':  forms.Select(choices=[], attrs={'class': 'form-control'}),
            'resultado': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'monto_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any'}),
            'interes_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any', 'readonly': 'readonly'}),
            'mora_pendiente': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'step': 'any', 'readonly': 'readonly'}),
            'fecha_promesa_pago': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado_cobranza':forms.Select(choices=[], attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'telefono_contacto':forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'fecha_limite_cuota':forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control', 'disabled':'disabled'})
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Opciones para el campo 'codigo_ingreso' (pueden venir de la base de datos)
        opciones_tipo_cobranza = [
            
            ('preventiva', 'Preventiva'),
            ('normal', 'Normal'),
            ('judicial', 'Judicial'),
            
        ]

        opciones_tipo_gestion = [        
            ('llamada', 'Llamada'),
            ('whatsapp', 'WhatsApp'),
            ('visita', 'Visita presencial'),
            ('correo', 'Correo electrónico'),

        ]

        opciones_resultados = [            
            ('Promesa de pago', 'Promesa de pago'),
            ('Pago realizado', 'Pago realizado'),
            ('No localizable', 'No localizable'),
            ('Negativa de pago', 'Negativa de pago'),
            ('Reprogramación de fecha', 'Reprogramación de fecha'),
            ('Traslado a Cobro Jurídico', 'Traslado a Cobro Jurídico')
            
        ]

        opciones_estado_cobranza = [            
            ('PENDIENTE', 'PENDIENTE'),
            ('INCUMPLIDO', 'INCUMPLIDO'),
            ('COMPLETADO', 'COMPLETADO'),

        ]

        # Asignar las opciones al widget 'Select'
        self.fields['tipo_cobranza'].widget.choices = opciones_tipo_cobranza
        self.fields['tipo_gestion'].widget.choices = opciones_tipo_gestion
        self.fields['resultado'].widget.choices = opciones_resultados
        self.fields['estado_cobranza'].widget.choices = opciones_estado_cobranza
        date_fields = ['fecha_gestion', 'fecha_promesa_pago', 'fecha_limite_cuota']
        for field in date_fields:
            self.fields[field].input_formats = ['%Y-%m-%d']


