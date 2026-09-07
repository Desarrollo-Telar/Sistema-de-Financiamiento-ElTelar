
# VIEWS DE CONDICIONES DE CREDITO
from django.shortcuts import render, get_object_or_404, redirect

# MODELS
from apps.financings.models import Credit

# DECORADORES
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie 
from project.decorador import  permiso_requerido
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


@login_required
@permiso_requerido('puede_registrar_condiciones_credito')
@ensure_csrf_cookie
def gestion_condiciones_credito_view(request, credit_id):

    credito = get_object_or_404(Credit, id=credit_id)
    
    if credito.is_paid_off:
        return redirect('financings:detail_credit', credito.id)
    
    return render(request, 'financings/credit/condiciones_credito.html', {'credito': credito, 'permisos': recorrer_los_permisos_usuario(request)})