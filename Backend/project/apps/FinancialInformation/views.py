from django.shortcuts import render, get_object_or_404

# FORMULARIO
from .forms import WorkingInformationForms,OtherSourcesOfIncomeForms,ReferenceForms

# MODELOS
from apps.customers.models import Customer
from .models import WorkingInformation, OtherSourcesOfIncome, Reference
# Create your views here.
