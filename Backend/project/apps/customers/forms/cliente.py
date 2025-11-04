from django import forms
from apps.customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

        # Lista de campos que quieres incluir en el formulario
        fields = [
            'first_name',
            'last_name',
            'type_identification',
            'identification_number',
            'lugar_emision_tipo_identificacion_departamento',
            'lugar_emision_tipo_identificacion_municipio',
            'email',
            'date_birth',
            'number_nit',
            'place_birth',
            'marital_status',
            'profession_trade',
            'gender',
            'nationality',
            'immigration_status_id',
            'telephone',
            'person_type',
            'new_asesor_credito',
            'status'
        ]

        # Diccionario de etiquetas (labels)
        labels = {
            'first_name': 'Nombre (*)',
            'last_name': 'Apellido (*)',
            'type_identification': 'Tipo de Identificación',
            'identification_number': 'Número de Identificación (*)',
            'email': 'Correo Electrónico (*)',
            'date_birth': 'Fecha de Nacimiento (*)',
            'number_nit': 'Número de NIT (*)',
            'place_birth': 'Lugar de Nacimiento (*)',
            'marital_status': 'Estado Civil (*)',
            'profession_trade': 'Profesión u Oficio',
            'gender': 'Género',
            'nationality': 'Nacionalidad',
            'telephone': 'Número de Teléfono (*)',
            'person_type': 'Tipo de Persona',
            'new_asesor_credito': 'Asesor del Crédito (*)',
            'status': 'Estado del Cliente',
            'immigration_status_id':'Condicion Migratoria (*)',
            'lugar_emision_tipo_identificacion_departamento': 'Departamento de Emision (*)',
            'lugar_emision_tipo_identificacion_municipio': 'Municipio de Emision (*)',
            
            
        }

        # Widgets personalizados
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_identification': forms.Select(attrs={'class': 'form-control'}),
            'identification_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_nit': forms.TextInput(attrs={'class': 'form-control'}),
            'place_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(choices=[], attrs={'class': 'form-control'}),
            'profession_trade': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control','type':'number', 'min':'0', 'maxlength':'8'}),
            'person_type': forms.Select(attrs={'class': 'form-control'}),
            'new_asesor_credito': forms.Select(attrs={'class': 'form-control asesor', 'required':'required'}),
            'status': forms.Select(
                choices=[
                    ('Revisión de documentos', 'Revisión de documentos'),
                    ('Aprobado', 'Aprobado'),
                    ('No Aprobado', 'No Aprobado'),
                    ('Posible Cliente', 'Posible Cliente'),
                    ('Dar de Baja', 'Dar de Baja'),
                ],
                attrs={'class': 'form-control'}
            ),
            'immigration_status_id':forms.Select(attrs={'class': 'form-control', 'requerid':'true'}),
            'lugar_emision_tipo_identificacion_departamento':  forms.Select(attrs={'class': 'form-control city2', 'required':'required'}),
            'lugar_emision_tipo_identificacion_municipio':  forms.Select(attrs={'class': 'form-control state2',  'required':'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opciones_estado_civil = [
            ('','---------'),
            ('SOLTER@','SOLTER@'),
            ('CASAD@','CASAD@'),
            ('DIVORCIAD@','DIVORCIAD@'),
            ('VIUD@','VIUD@'),
            ('UNIÓN DE HECHO','UNIÓN DE HECHO')

        ]
        self.fields['marital_status'].widget.choices = opciones_estado_civil
        self.fields['status'].required = False
        # Asignar valor por defecto del modelo
        if not self.initial.get('status'):
            self.initial['status'] = 'Posible Cliente'
