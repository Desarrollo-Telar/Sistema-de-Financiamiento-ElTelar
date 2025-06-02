from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import  Egress


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan
from apps.financings.tareas_ansicronicas import ver_caso_de_gastos
# MENSAJES
from django.contrib import messages

@login_required
@usuario_activo
def pendiente_egresos_vincular(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.filter(status=False).order_by('-id')
    page_obj = paginacion(request, object_list)
    ver_caso_de_gastos()
    
    context = {
        'title':'EL TELAR - EGRESOS / PENDIENTES DE VINCULAR',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        
    }
        
    return render(request, template_name, context)

@login_required
@usuario_activo
def egresos_vinculados(request):
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.filter(status=True).order_by('-id')
    page_obj = paginacion(request, object_list)
    cambiar_plan()
    context = {
        'title':'EL TELAR - EGRESOS / VINCULADOS',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        
    }
        
    return render(request, template_name, context)