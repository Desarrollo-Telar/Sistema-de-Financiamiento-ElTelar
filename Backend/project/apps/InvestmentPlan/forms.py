from django import forms

# Models
from .models import InvestmentPlan

class InvestmentPlanForms(forms.ModelForm):
    class Meta:
        model = InvestmentPlan

        fields = [
            'type_of_product_or_service',
            'total_value_of_the_product_or_service',
            'plazo',
            'tasa_interes',
            'forma_de_pago',
            'fecha_inicio',
            'investment_plan_description',
            'initial_amount',
            'monthly_amount'
            
        ]

        labels = {
            'type_of_product_or_service': 'Tipo de producto o servicio',
            'total_value_of_the_product_or_service': 'Valor total del producto o servicio',
            'investment_plan_description': 'Descripción del plan de inversión',
            'initial_amount': 'Monto inicial a manejar en el producto o servicio',
            'monthly_amount': 'Monto mensual a manejar en el producto o servicio',
            'transfers_or_transfer_of_funds': 'Transferencia o trasalado de fondos (Si o No)',
            'type_of_transfers_or_transfer_of_funds':'Tipo de transferencias o traslado de fondos',
            'tasa_interes': 'Tasa de Interes Anual'
        }

        widgets = {
            'type_of_product_or_service':forms.Select(attrs={'class':'form-control'}),
            'total_value_of_the_product_or_service':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0'}),
            'investment_plan_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'initial_amount':forms.TextInput(attrs={'class':'form-control'}),
            'monthly_amount':forms.TextInput(attrs={'class':'form-control'}),
            'transfers_or_transfer_of_funds':forms.CheckboxInput(),
            'type_of_transfers_or_transfer_of_funds':forms.Select(attrs={'class':'form-control'}),
            'plazo':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0','step':'1'}),
            'tasa_interes':forms.TextInput(attrs={'class':'form-control','type':'number', 'min':'0','step':'1'}),
            'forma_de_pago':forms.Select(attrs={'class':'form-control'}),
            'fecha_inicio':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            

        }