from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def role_permission(request):
    template_name = 'role&permission/index.html'
    context = {
        'title': 'EL TELAR - ROLES Y PERMISOS'
    }
    return render(request, template_name, context)