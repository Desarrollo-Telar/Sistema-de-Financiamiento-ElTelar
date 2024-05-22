from django import forms

# Models
from .models import Address

class AddressForms(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = {}