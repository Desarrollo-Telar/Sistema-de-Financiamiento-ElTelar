from django.shortcuts import render

# Decorador
from django.contrib.auth.decorators import login_required

# Modelo
from .models import Role

# Create your views here.
@login_required
def role_permission(request):
    template_name = 'role&permission/index.html'
    role = Role.objects.all()
    context = {
        'title': 'EL TELAR - ROLES Y PERMISOS',
        'role_list':role,
    }
    return render(request, template_name, context)