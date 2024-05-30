
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Metodos HTTP
from django.http import HttpResponse

# Modelos
from .models import VerificationToken, User

# Formulario
from .forms import RegistroForm, UpdateUserForm, ChangePasswordForm

# LIBRERIAS PARA EL CRUD
from django.views.generic import CreateView, UpdateView, DeleteView, View

# URL
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

# Paginacion
from project.pagination import paginacion

# Login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

@login_required
@usuario_activo
def list_user(request):
    template_name = 'user/list_user.html'
    users = User.objects.all().order_by('-id')
    # PAGINACION
    page_obj = paginacion(request,users)

    context = {
        'title':'EL TELAR - USUARIOS',
        'users_list':users,
        'page_obj':page_obj,
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def profile(request):
    template_name = 'user/user_profile.html'
    users =  get_object_or_404(User, username=request.user.username)
    
    context = {
        'title':'EL TELAR - PERFIL {}'.format(users),
        'user':users,
    }
    return render(request, template_name, context)


class userCreateView(CreateView):
    template_name = 'user/add_user.html'
    form_class = RegistroForm
    model = User

    success_url = reverse_lazy(('users:users'))

    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Nuevo Usuario'
        context['accion'] = 'Añadir Usuario'
        return context


class userUpdateView(UpdateView):
    template_name = 'user/add_user.html'
    form_class = UpdateUserForm
    model = User

    success_url = reverse_lazy(('users:users'))

    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Usuario'
        context['accion'] = 'Actualizar Usuario'
        return context


class ChangePassword(View):
    template_name ='user/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('index')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form':self.form_class, 
            'title': 'CAMBIAR CONTRASEÑA',
            'info': 'CAMBIAR CONTRASEÑA'
            })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(pk = request.user.pk)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                contra = form.cleaned_data.get('password1')
                user.save()
                user = authenticate(username=request.user.username, password=contra)
                login(self.request, user)

                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {
            'form':form, 
            'title': 'CAMBIAR CONTRASEÑA',
            'info': 'CAMBIAR CONTRASEÑA'
            })