
from django.shortcuts import render, get_object_or_404, redirect

from apps.financings.tareas_ansicronicas import ver_cuotas_no_cargadas

def async_view_banco(request):
    ver_cuotas_no_cargadas()
    return redirect('financings:list_bank')
    
    
def async_view_boletas(request):
    ver_cuotas_no_cargadas()
    return redirect('financings:list_payment')
    