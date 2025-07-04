from django import forms

# Modelo
from .models import Role
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            'role_name',
            'permissions',
            'description',
        ]

        labels = {
            'role_name': 'Rol',
            'permissions':'Permisos',
            'description':'Descripcion',

        }

        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'permissions': forms.CheckboxSelectMultiple(attrs={'class':''}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }