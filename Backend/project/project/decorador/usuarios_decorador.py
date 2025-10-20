from django.contrib.auth import logout
from django.shortcuts import redirect

# htpp
from django.http import HttpResponseNotFound
def usuario_activo(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user

        sucursal = getattr(request,'sucursal_actual',None)
    
        if not user.status:
            logout(request)
            return redirect('login')
        
        if sucursal is None:
            return redirect('sucursal:clasificacion')
        
        if user.sucursal is not None:

            sucursal = getattr(request,'sucursal_actual',None)
            if sucursal is None:
                return redirect('sucursal:clasificacion')
            
            request.session['sucursal_id'] = user.sucursal.id

        
        
        
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