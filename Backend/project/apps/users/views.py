
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import VerificationToken, User

# import get_object_or_404()
from django.shortcuts import get_object_or_404

# Formulario
from .forms import RegistroForm, UpdateUserForm
from django.views import generic
from django.urls import reverse_lazy, reverse

@login_required
def list_user(request):
    template_name = 'user/list_user.html'
    users = User.objects.all()
    print(users)
    context = {
        'title':'EL TELAR - USUARIOS',
        'users_list':users,
    }
    return render(request, template_name, context)

@login_required
def profile(request):
    template_name = 'user/user_profile.html'
    users =  get_object_or_404(User, username=request.user.username)
    print(users)
    context = {
        'title':'EL TELAR - PERFIL {}'.format(users),
        'users_list':users,
    }
    return render(request, template_name, context)

class userCreateView(generic.CreateView):
    template_name = 'user/add_user.html'
    form_class = RegistroForm
    model = User

    success_url = reverse_lazy(('users:users'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Nuevo Usuario'
        context['accion'] = 'Añadir Usuario'
        return context

class userUpdateView(generic.UpdateView):
    template_name = 'user/add_user.html'
    form_class = UpdateUserForm
    model = User

    success_url = reverse_lazy(('users:users'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Usuario'
        context['accion'] = 'Actualizar Usuario'
        return context