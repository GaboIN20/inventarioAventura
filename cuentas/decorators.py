from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if hasattr(request.user, 'perfil') and request.user.perfil.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'Acceso denegado: no tienes permisos para esta sección.')
            return redirect('dashboard')
        return _wrapped_view
    return decorator