from django.shortcuts import render

# Decorador
from django.contrib.auth.decorators import login_required

# Modelo
from .models import Role

# Formulario
from .forms import RoleForm

# CRUD
from django.views.generic.edit import CreateView

# LIBRERIAS PARA REDERICCIONAR
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

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

class AddRole(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'role&permission/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Rol'
        context['accion'] = 'Crear Rol'

        return context

    success_url = reverse_lazy('roles_permissions:roles_permissions')
