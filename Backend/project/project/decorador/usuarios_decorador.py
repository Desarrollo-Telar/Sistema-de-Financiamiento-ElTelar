from django.contrib.auth import logout
from django.shortcuts import redirect

# htpp
from django.http import HttpResponseNotFound
def usuario_activo(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.status:
            logout(request)
            return redirect('login')
        return funcion(request, *args, **kwargs)
    return wrapper

def usuario_administrador(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        

        return funcion(request, *args, **kwargs)
    return wrapper

def usuario_secretaria(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user
        

        return funcion(request, *args, **kwargs)
    return wrapper

def usuario_contabilidad(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user
        

        return funcion(request, *args, **kwargs)
    return wrapper