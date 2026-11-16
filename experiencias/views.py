from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, Experiencia, Inscripcion
from .forms import CategoriaForm, ExperienciaForm
from cuentas.decorators import rol_requerido

# --- CATEGORÍAS (Solo ADMIN) ---
@rol_requerido(['ADMIN'])
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'experiencias/lista_categorias.html', {'categorias': categorias})

@rol_requerido(['ADMIN'])
def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('lista_categorias')
    return render(request, 'experiencias/form_generico.html', {'form': form, 'titulo': 'Nueva Categoría'})

@rol_requerido(['ADMIN'])
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('lista_categorias')
    return render(request, 'experiencias/form_generico.html', {'form': form, 'titulo': 'Editar Categoría'})

@rol_requerido(['ADMIN'])
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, 'Categoría eliminada.')
    return redirect('lista_categorias')

# --- EXPERIENCIAS (ADMIN ve todo, GUIA solo las suyas) ---[cite: 1]
@rol_requerido(['ADMIN', 'GUIA'])
def lista_experiencias(request):
    if request.user.perfil.rol == 'ADMIN':
        experiencias = Experiencia.objects.select_related('categoria', 'creador').all()
    else:
        experiencias = Experiencia.objects.filter(creador=request.user).select_related('categoria')
    return render(request, 'experiencias/lista_experiencias.html', {'experiencias': experiencias})

@rol_requerido(['ADMIN', 'GUIA'])
def crear_experiencia(request):
    form = ExperienciaForm(request.POST or None)
    if form.is_valid():
        exp = form.save(commit=False)
        exp.creador = request.user
        exp.save()
        messages.success(request, 'Experiencia registrada exitosamente.')
        return redirect('lista_experiencias')
    return render(request, 'experiencias/form_generico.html', {'form': form, 'titulo': 'Nueva Experiencia'})

@rol_requerido(['ADMIN', 'GUIA'])
def editar_experiencia(request, id):
    exp = get_object_or_404(Experiencia, id=id)
    # Restricción: Guía solo edita las suyas[cite: 1]
    if request.user.perfil.rol == 'GUIA' and exp.creador != request.user:
        messages.error(request, 'Solo puedes editar experiencias creadas por ti.')
        return redirect('lista_experiencias')

    form = ExperienciaForm(request.POST or None, instance=exp)
    if form.is_valid():
        form.save()
        messages.success(request, 'Experiencia actualizada.')
        return redirect('lista_experiencias')
    return render(request, 'experiencias/form_generico.html', {'form': form, 'titulo': 'Editar Experiencia'})

@rol_requerido(['ADMIN']) # Guía NO puede eliminar[cite: 1]
def eliminar_experiencia(request, id):
    exp = get_object_or_404(Experiencia, id=id)
    exp.delete()
    messages.success(request, 'Experiencia eliminada.')
    return redirect('lista_experiencias')

# --- CATÁLOGO Y RESERVAS (TURISTA y ADMIN) ---[cite: 1]
@rol_requerido(['TURISTA'])
def catalogo_turista(request):
    experiencias = Experiencia.objects.filter(categoria__estado=True).select_related('categoria', 'creador')
    mis_ids = Inscripcion.objects.filter(turista=request.user).values_list('experiencia_id', flat=True)
    return render(request, 'experiencias/catalogo.html', {'experiencias': experiencias, 'mis_ids': mis_ids})

@rol_requerido(['TURISTA'])
def inscribir_experiencia(request, id):
    exp = get_object_or_404(Experiencia, id=id)
    if exp.cupos_disponibles() <= 0:
        messages.error(request, 'No quedan cupos disponibles para esta actividad.')
    elif Inscripcion.objects.filter(turista=request.user, experiencia=exp).exists():
        messages.warning(request, 'Ya estás inscrito en esta experiencia.')
    else:
        Inscripcion.objects.create(turista=request.user, experiencia=exp, estado_pago='PENDIENTE')
        # Estado de colección en sesión[cite: 1]
        historial = request.session.get('historial_vistos', [])
        historial.append(exp.titulo)
        request.session['historial_vistos'] = historial
        messages.success(request, f'Reserva realizada para {exp.titulo}.')
    return redirect('mis_reservas')

@rol_requerido(['TURISTA', 'ADMIN'])
def mis_reservas(request):
    if request.user.perfil.rol == 'ADMIN':
        reservas = Inscripcion.objects.select_related('turista', 'experiencia').all()
    else:
        reservas = Inscripcion.objects.filter(turista=request.user).select_related('experiencia')
    return render(request, 'experiencias/mis_reservas.html', {'reservas': reservas})

@rol_requerido(['ADMIN', 'TURISTA'])
def confirmar_pago(request, id):
    reserva = get_object_or_404(Inscripcion, id=id)
    if request.user.perfil.rol == 'ADMIN' or reserva.turista == request.user:
        reserva.estado_pago = 'CONFIRMADO'
        reserva.save()
        messages.success(request, 'Pago confirmado.')
    return redirect('mis_reservas')