from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil
from .forms import RegistroForm
from .decorators import rol_requerido

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            rol = user.perfil.rol if hasattr(user, 'perfil') else 'TURISTA'
            request.session['rol_usuario'] = rol
            request.session['historial_vistos'] = []
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'cuentas/login.html')

def logout_view(request):
    request.session.flush() 
    logout(request)
    return redirect('home')

def registro_turista(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Perfil.objects.create(
                usuario=user,
                rol='TURISTA', # Registro público solo crea turistas
                telefono=form.cleaned_data.get('telefono')
            )
            messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
        form.fields.pop('rol') # Ocultar selector de rol en registro público
    return render(request, 'cuentas/registro.html', {'form': form})

@rol_requerido(['ADMIN'])
def lista_usuarios(request):
    usuarios = User.objects.select_related('perfil').all()
    return render(request, 'cuentas/lista_usuarios.html', {'usuarios': usuarios})

@rol_requerido(['ADMIN'])
def crear_usuario_admin(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Perfil.objects.create(
                usuario=user,
                rol=form.cleaned_data['rol'],
                telefono=form.cleaned_data.get('telefono')
            )
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/form_usuario.html', {'form': form, 'titulo': 'Nuevo Usuario'})

@rol_requerido(['ADMIN'])
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if usuario != request.user:
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
    return redirect('lista_usuarios')