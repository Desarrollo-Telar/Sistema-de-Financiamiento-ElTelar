
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator


# Modelos
from .models import  User

# Formulario
from .forms import RegistroForm, UpdateUserForm, ChangePasswordForm

# LIBRERIAS PARA EL CRUD
from django.views.generic import View

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView

from django.db.models import Q

# URL
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

# Paginacion
from project.pagination import paginacion

# Login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from django.apps import apps
from django.contrib import messages

# CONFIGURACION
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# ----- DESACTIVAR A UN USUARIO ---- #
@login_required
@permiso_requerido('puede_dar_de_baja_un_usuario')
def deactivate(request, id):
    
    user = get_object_or_404(User, id=id)
    if request.user == user:
        return redirect('users:users')
    
    user.status = False
    user.save()
    return redirect('users:users')
    
@login_required
@permiso_requerido('puede_habilitar_usuario')
def habilitar_usuario(request,id):
    user = get_object_or_404(User, id=id)
    user.status = True
    user.save()
    return redirect('users:users')

# ----- LISTADO DE USUARIOS ----- #
@login_required
@permiso_requerido('puede_ver_registro_usuarios')
def list_user(request):
    template_name = 'user/list_user.html'
    users = User.objects.all().order_by('user_code')
    # PAGINACION
    page_obj = paginacion(request,users)

    context = {
        'title':'LISTADO DE REGISTRO DE USUARIOS',
        'object_list':page_obj,
        'page_obj':page_obj,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

# ----- PERFIL DE USUARIOS ----- #
@login_required
@permiso_requerido('puede_ver_perfil_usuario')
def profile(request):
    template_name = 'user/user_profile.html'
    users =  get_object_or_404(User, username=request.user.username)
    
    context = {
        'title':'PERFIL {}'.format(users),
        'user':users,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

# ----- CREACION DE USUARIOS ----- #
class userCreateView(CreateView):
    template_name = 'user/add_user.html'
    form_class = RegistroForm
    model = User

    success_url = reverse_lazy(('users:users'))

    @method_decorator([permiso_requerido("puede_crear_usuario")])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Nuevo Usuario'
        context['accion'] = 'Añadir Usuario'
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

# ----- MODIFICAR INFORMACION DE USUARIOS ----- #
class userUpdateView(UpdateView):
    template_name = 'user/update_user.html'
    form_class = UpdateUserForm
    model = User

    success_url = reverse_lazy(('users:users'))

    @method_decorator([permiso_requerido("puede_editar_usuario")])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Usuario'
        context['accion'] = 'Actualizar Usuario'
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

# ----- CAMBIO DE CONTRASEÑA DE USUARIOS ----- #
class ChangePassword(View):
    template_name ='user/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('index')
    

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form':self.form_class, 
            'permisos':recorrer_los_permisos_usuario(request),
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
            'permisos':recorrer_los_permisos_usuario(request),
            'info': 'CAMBIAR CONTRASEÑA'
            })

# ----- MODULO QUE CAMBIA LA CONTRASEÑA A USUARIOS ----- #
@permiso_requerido('puede_editar_usuario')
def change_password_user(request, id):
    template_name ='user/change_password.html'
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)  # Crear una instancia del formulario con los datos POST
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            messages.success(request, 'Contraseña cambiada exitosamente')
            return redirect('users:users')
        else:
            messages.error(request, 'No se pudo realizar el cambio, verifique bien sus credenciales')
    
    form = ChangePasswordForm()  # Crear una instancia del formulario vacía si es una solicitud GET

    context = {
        'form': form,
        'permisos':recorrer_los_permisos_usuario(request),
        'info': 'CAMBIAR CONTRASEÑA'
    }
    return render(request, template_name, context)

# ----- MODULO QUE BUSCA A LOS USUARIOS ----- #
class UserSearch(ListView):
    template_name = 'user/search.html'

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()
            
            # Definir los filtros utilizando Q objects
            filters = (
                Q(first_name__icontains=query) | 
                Q(username__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(type_identification__icontains=query) |
                Q(gender__icontains=query) |
                Q(email__icontains=query) |
                Q(telephone__icontains=query) |
                Q(identification_number__icontains=query) |
                Q(nationality__icontains=query) 
            )
            
            # Filtrar los objetos Customer usando los filtros definidos
            return User.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return User.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator([permiso_requerido("puede_ver_registro_usuarios")])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

# ----- VER DETALLES DE UN USUARIOS ----- #
@login_required
@permiso_requerido('puede_ver_detalle_usuario')
def detail_user(request,username):
    user_id = get_object_or_404(User, username=username)
    template_name = 'user/user_profile.html'
    context = {
        'title':'{}'.format(user_id),
        'user':user_id,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)