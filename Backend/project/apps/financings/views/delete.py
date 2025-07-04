from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Disbursement


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_secretaria, usuario_administrador
from django.utils.decorators import method_decorator



@login_required
@usuario_activo
def delete_desembolso(request, id):
    desembolso = get_object_or_404(Disbursement, id=id)
    desembolso.delete()
    return redirect('financings:list_disbursement')


@login_required
@usuario_activo
def delete_credit(request, id):
    credit = get_object_or_404(Credit,id=id)
    credit.delete()
    return redirect('financings:list_credit')