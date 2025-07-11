from django import forms

# Models
from .models import Reference, OtherSourcesOfIncome, WorkingInformation, Reference

class WorkingInformationForms(forms.ModelForm):
    class Meta:
        model = WorkingInformation
        fields = [
            'position',
            'company_name',
            'start_date',            
            'salary',
            'working_hours',
            'phone_number',
            'source_of_income',
            'income_detail',
            'employment_status',
            'description',
        ]

        labels = {
            'position':'Puesto',
            'company_name': 'Nombre de la Empresa',
            'start_date': 'Fecha de Inicio',
            'description': 'Detalles',
            'salary': 'Salario',            
            'working_hours': 'Horario de Trabajo',
            'phone_number': 'Numeor de telefono',
            'source_of_income': 'Fuentes de Ingreso',
            'income_detail': 'Detalles de ingreso',
            'employment_status':'Estado laboral',
        }

        widgets = {
            'position': forms.TextInput(attrs={'class':'form-control'}),
            'company_name':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.TextInput(attrs={'class':'form-control', 'type':'date'}),
            
            'source_of_income': forms.Select(attrs={'class':'form-control'}),
            'employment_status':forms.Select(attrs={'class':'form-control'}),

            'description':forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'income_detail':forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'salary': forms.TextInput(attrs={'class':'form-control', 'type':'number','min':'0', 'step':'any'}),
            'working_hours': forms.Select(choices=[],attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'type':'number','min':'0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        opciones_horario_trabajo = [
            ('', '--------------'),
            ('VESPERTINA','VESPERTINA'),
            ('NOCTURNO','NOCTURNO'),
            ('FIN DE SEMANA','FIN DE SEMANA'),
        ]

        self.fields['working_hours'].widget.choices = opciones_horario_trabajo


class OtherSourcesOfIncomeForms(forms.ModelForm):
    class Meta:
        model = OtherSourcesOfIncome

        fields = [
            'source_of_income',
            'nit',
            'phone_number',
            'salary'
        ]

        labels = {
            'source_of_income': 'Fuente de ingreso',
            'nit': 'NIT',
            'phone_number': 'Numero de telefono',
            'salary':'Salario',

        }


        widgets = {
            'source_of_income':forms.TextInput(attrs={'class':'form-control'}),
            'nit': forms.TextInput(attrs={'class':'form-control',}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'type':'number','min':'0'}),
            'salary': forms.TextInput(attrs={'class':'form-control', 'type':'number','min':'0', 'step':'any'}),
        }

class ReferenceForms(forms.ModelForm):
    class Meta:
        model = Reference

        fields = [
            'full_name',
            'phone_number',
            
        ]
        labels = {
            'full_name':'Nombre Completo',
            'phone_number':'Número de Teléfono',
            'reference_type':'Tipo de Referencia'

        }
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'reference_type':forms.Select(attrs={'class':'form-control'}),
        }
