from django.contrib.auth import logout
from django.shortcuts import redirect

def usuario_activo(funcion):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.status:
            logout(request)
            return redirect('login')
        return funcion(request, *args, **kwargs)
    return wrapper
