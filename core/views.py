from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from experiencias.models import Experiencia, Inscripcion
from django.contrib.auth.models import User
from cuentas.models import Perfil  

def home(request):
    experiencias_destacadas = Experiencia.objects.filter(categoria__estado=True)[:6]
    return render(request, 'core/home.html', {'experiencias': experiencias_destacadas})

@login_required
def dashboard(request):
    perfil, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'rol': 'ADMIN' if request.user.is_superuser else 'TURISTA'}
    )
    rol = perfil.rol
    
    context = {'rol': rol}
    if rol == 'ADMIN':
        context['total_usuarios'] = User.objects.count()
        context['total_experiencias'] = Experiencia.objects.count()
        context['total_reservas'] = Inscripcion.objects.count()
    elif rol == 'GUIA':
        context['mis_experiencias'] = Experiencia.objects.filter(creador=request.user).count()
    else:
        context['mis_reservas'] = Inscripcion.objects.filter(turista=request.user).count()
    return render(request, 'core/dashboard.html', context)