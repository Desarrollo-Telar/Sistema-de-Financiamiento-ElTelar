from django import forms

# Models
from .models import InvestmentPlan

class InvestmentPlanForms(forms.ModelForm):
    class Meta:
        model = InvestmentPlan

        fields = [
            'type_of_product_or_service',
            'tipo_pagare',
            'credito_anterior_vigente',
            'fiador',
            'total_value_of_the_product_or_service',
            'plazo',
            'tasa_interes',
            'forma_de_pago',
            'fecha_inicio',
            'investment_plan_description',
            'initial_amount',
            'monthly_amount',            
            
        ]

        labels = {
            'type_of_product_or_service': 'Tipo de producto o servicio',
            'total_value_of_the_product_or_service': 'Valor total del producto o servicio',
            'investment_plan_description': 'Descripción del plan de inversión',
            'initial_amount': 'Monto inicial a manejar en el producto o servicio',
            'monthly_amount': 'Monto mensual a manejar en el producto o servicio',
            'transfers_or_transfer_of_funds': 'Transferencia o trasalado de fondos (Si o No)',
            'type_of_transfers_or_transfer_of_funds':'Tipo de transferencias o traslado de fondos',
            'tasa_interes': 'Tasa de Interes Anual',
            'tipo_pagare':'Tipo de Pagare',
            'credito_anterior_vigente':'Credito Anterior',
            'fiador':'Fiador',
           
        }

        widgets = {
            'type_of_product_or_service':forms.Select(attrs={'class':'form-control'}),
            'total_value_of_the_product_or_service':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0'}),
            'investment_plan_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'initial_amount':forms.TextInput(attrs={'class':'form-control'}),
            'monthly_amount':forms.TextInput(attrs={'class':'form-control'}),
            'transfers_or_transfer_of_funds':forms.CheckboxInput(),
            'type_of_transfers_or_transfer_of_funds':forms.Select(attrs={'class':'form-control'}),
            'plazo':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0'}),
            'tasa_interes':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0'}),
            'forma_de_pago':forms.Select(attrs={'class':'form-control'}),
            'fecha_inicio':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'tipo_pagare': forms.Select(choices=[], attrs={'class': 'form-control'}),

            'credito_anterior_vigente':forms.Select(choices=[], attrs={'class': 'form-control credito_vigente'}),
            'fiador':forms.Select(choices=[], attrs={'class': 'form-control customer_id'}),
            

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        opciones_tipo_pagare = [         
            ('Normal', 'Normal'),
            ('Fiador', 'Fiador'),
            ('Restructuracion', 'Restructuracion')
            
        ]
        self.fields['tipo_pagare'].widget.choices = opciones_tipo_pagare